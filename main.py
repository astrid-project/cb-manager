from configparser import ConfigParser
from elasticsearch_dsl import connections
from falcon_auth import FalconAuthMiddleware, BasicAuthBackend
from falcon_marshmallow import Marshmallow
from route import AgentCatalog, AgentInstance, Connection, Data, ExecEnv, ExecEnvType, NetworkLink, NetworkLinkType
from utils import wrap
import argparse
import falcon
import waitress


config_parser = ConfigParser()
config_parser.read('config.ini')

title = config_parser.get('info', 'title')
description = config_parser.get('info', 'description')
version = config_parser.get('info', 'version')

cb_port = config_parser.get('context-broker', 'port')

es_endpoint = config_parser.get('elasticsearch', 'endpoint')
es_timeout = config_parser.get('elasticsearch', 'timeout')


print(f'{title} v{version}')


parser = argparse.ArgumentParser(
    prog='python3 {__FILENAME__}', description=f'{title}: {description}')
parser.add_argument('--port', '-p', type=int,
                    help='TCP Port of the REST Server', default=cb_port)
parser.add_argument('--es-endpoint', '-e', type=str,
                    help='Elastic Search server hostname/IP:port', default=es_endpoint)
parser.add_argument('--es-timeout', '-t', type=int,
                    help='Timeout seconds for the connection to Elastic Search', default=es_timeout)
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
    api = falcon.API(middleware=[
        FalconAuthMiddleware(BasicAuthBackend(
            lambda username, password: {'username': username})),
        Marshmallow()
    ])

    connections.create_connection(hosts=args.es_endpoint, timeout=args.es_timeout)

    for RouteResource in AgentCatalog, AgentInstance, Connection, Data, ExecEnv, ExecEnvType, NetworkLink, NetworkLinkType:
        RouteResource.doc_cls.init()
        for route in wrap(RouteResource.route):
            api.add_route(route, RouteResource())

    waitress.serve(api, host='0.0.0.0', port=args.port)
