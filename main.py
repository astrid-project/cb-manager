from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from configparser import ConfigParser
from elasticsearch_dsl import connections
from falcon_auth import FalconAuthMiddleware, BasicAuthBackend
from falcon_apispec import FalconPlugin
from falcon_marshmallow import Marshmallow
from resource import *
from schema import *
from swagger_ui import falcon_api_doc
from utils import *
import argparse
import falcon
import hashlib
import json
import waitress


config_parser = ConfigParser()
config_parser.read('config.ini')

title = config_parser.get('info', 'title')
description = config_parser.get('info', 'description')
version = config_parser.get('info', 'version')

cb_port = config_parser.get('context-broker', 'port')

auth_username = config_parser.get('auth', 'username')
auth_password = config_parser.get('auth', 'password')

es_endpoint = config_parser.get('elasticsearch', 'endpoint')
es_timeout = config_parser.get('elasticsearch', 'timeout')


print(f'{title} v{version}')

<
parser = argparse.ArgumentParser(
    prog='python3 {__FILENAME__}', description=f'{title}: {description}')

parser.add_argument('--port', '-p', type=int,
                    help='TCP Port of the REST Server', default=cb_port)

parser.add_argument('--auth-username', '-u', type=str,
                    help='Authorized username', default=auth_username)
parser.add_argument('--auth-password', '-a', type=str,
                    help='Authorized password', default=auth_password)

parser.add_argument('--es-endpoint', '-e', type=str,
                    help='Elasticsearch server hostname/IP:port', default=es_endpoint)
parser.add_argument('--es-timeout', '-s', type=int,
                    help='Timeout seconds for the connection to Elasticsearch', default=es_timeout)

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
    def auth(username, password):
        if username == args.auth_username and hashlib.sha224(password.encode('utf-8')).hexdigest() == args.auth_password:
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
        NetworkLinkTypeResource, NetworkLinkTypeSelectedResource)

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

    for schema in BadRequestSchema, UnauthorizedSchema:
        api_spec.components.schema(schema.__name__, schema=schema)

    connections.create_connection(hosts=args.es_endpoint, timeout=args.es_timeout)

    for Resource in resource_set:
        Resource.doc_cls.init()
        for route in wrap(Resource.routes):
            resource = Resource()
            api.add_route(route, resource)
            api_spec.path(resource=resource)

    with open('./api/schema.yaml', 'w') as file:
        file.write(api_spec.to_yaml())

    with open('./api/schema.json', 'w') as file:
        file.write(json.dumps(api_spec.to_dict(), indent=2))

    falcon_api_doc(api, config_path='./api/schema.json', url_prefix='/api/doc', title='API doc')

    waitress.serve(api, host='0.0.0.0', port=args.port)
