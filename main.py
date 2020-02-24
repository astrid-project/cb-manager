from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from configparser import ConfigParser
from elasticsearch_dsl import connections
from falcon_apispec import FalconPlugin
from falcon_auth import FalconAuthMiddleware, BasicAuthBackend
from falcon_marshmallow import Marshmallow
from resource import *
from schema import *
from swagger_ui import falcon_api_doc

import argparse
import falcon
import hashlib
import json
import time
import utils
import waitress


config_parser = ConfigParser()
config_parser.read('config.ini')

title = config_parser.get('info', 'title')
description = config_parser.get('info', 'description')
version = config_parser.get('info', 'version')

cb_host = config_parser.get('context-broker', 'host')
cb_port = config_parser.get('context-broker', 'port')

hb_timeout = config_parser.get('hearthbeat', 'timeout')
hb_period = config_parser.get('hearthbeat', 'period')

es_endpoint = config_parser.get('elasticsearch', 'endpoint')
es_timeout = config_parser.get('elasticsearch', 'timeout')
es_retry_period = config_parser.get('elasticsearch', 'retry-period')

dev_debug = config_parser.get('dev', 'debug')
dev_username = config_parser.get('dev', 'username')
dev_password = config_parser.get('dev', 'password')


print(f'{title} v{version}')


parser = argparse.ArgumentParser(
    prog='python3 {__FILENAME__}', description=f'{title}: {description}')

parser.add_argument('--host', '-o', type=str,
                    help='Hostname/IP of the REST Server', default=cb_host)
parser.add_argument('--port', '-p', type=int,
                    help='TCP Port of the REST Server', default=cb_port)

parser.add_argument('--hb-timeout', '-b', type=float,
                    help='Timeout (in seconds) for heartbeat with LCPs', default=hb_timeout)
parser.add_argument('--hb-period', '-r', type=float,
                    help='Period (in seconds) per the hearthbeat with the LCPs', default=hb_period)

parser.add_argument('--es-endpoint', '-e', type=str,
                    help='Elasticsearch server hostname/IP:port', default=es_endpoint)
parser.add_argument('--es-timeout', '-s', type=float,
                    help='Timeout (in seconds) for the connection to Elasticsearch', default=es_timeout)
parser.add_argument('--es-retry_period', '-y', type=float,
                    help='Period (in seconds) to retry the connection to Elasticsearch', default=es_retry_period)

parser.add_argument('--dev-debug', '-d', help='Enable debug',
                    action='store_true')
parser.add_argument('--dev-username', '-u', type=str,
                    help='Authorized username', default=dev_username)
parser.add_argument('--dev-password', '-a', type=str,
                    help='Authorized password', default=dev_password)

parser.add_argument('--write-config', '-w', help='Write options to config.ini',
                    action='store_true')
parser.add_argument('--version', '-v', help='Show version',
                    action='store_const', const=version)

args = parser.parse_args()

if args.write_config:
    config_parser.set('context-broker', 'port', args.port)
    config_parser.set('elasticsearch', 'endpoint', args.es_endpoint)
    config_parser.set('elasticsearch', 'timeout', args.es_timeout)
    with open('config.ini', 'w') as f:
            config_parser.write(f)

if args.version is not None:
    print(args.version)
else:
    args.dev_debug = args.dev_debug or dev_debug

    def elastic_connection():
        try:
            print(f'Info: start connection to Elasticsearch ({args.es_endpoint}).')
            connections.create_connection(hosts=args.es_endpoint, timeout=args.es_timeout)
        except:
            print(f'Error: connection to Elasticsearch ({args.es_endpoint}) not possible.')
            print(f'Info: try again in {args.es_retry_period} seconds.')
            time.sleep(args.es_retry_period)
            elastic_connection()
        else:
            print(f'Success: connection to Elasticsearch ({args.es_endpoint}) established.')


    def auth(username, password):
        auth_data = [(args.dev_username, args.dev_password)]
        exec_env = ExecEnvDocument.get(id=username, ignore=404)
        if exec_env is not None and exec_env.lcp.last_heartbeat is not None:
            auth_data.append((exec_env.meta.id, exec_env.lcp.cb_password))
        if (username, utils.hash(password)) in auth_data:
            return {'username': username}
        else:
            False

    api = falcon.API(middleware=[
        FalconAuthMiddleware(BasicAuthBackend(auth), exempt_routes=['/api/doc', '/api/doc/swagger.json']),
        Marshmallow()
    ])

    resource_set = (AgentCatalogResource, AgentCatalogSelectedResource,
        AgentInstanceResource, AgentInstanceSelectedResource,
        ConnectionResource, ConnectionSelectedResource,
        DataResource, DataSelectedResource,
        ExecEnvResource, ExecEnvSelectedResource,
        ExecEnvTypeResource, ExecEnvTypeSelectedResource,
        NetworkLinkResource, NetworkLinkSelectedResource,
        NetworkLinkTypeResource, NetworkLinkTypeSelectedResource,
        PkgResource)

    tags = []
    for Resource in resource_set:
        tags.append(Resource.tag)

    api_spec = APISpec(
        title=title,
        version=version,
        openapi_version='2.0',
        produces=['application/json'],
        consumes=['application/json'],
        tags=tags,
        plugins=[
            FalconPlugin(api),
            MarshmallowPlugin(),
        ],
    )

    elastic_connection()

    for Resource in resource_set:
        resource = Resource(args)
        for route in utils.wrap(Resource.routes):
            api.add_route(route, resource)
            api_spec.path(resource=resource)
            print(f'Success: {route} endpoint configured.')

    with open('./api/schema.yaml', 'w') as file:
        file.write(api_spec.to_yaml())

    with open('./api/schema.json', 'w') as file:
        file.write(json.dumps(api_spec.to_dict(), indent=2))

    falcon_api_doc(api, config_path='./api/schema.json', url_prefix='/api/doc', title='API doc')

    waitress.serve(api, host=args.host, port=args.port)
