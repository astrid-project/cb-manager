title = 'ASTRID Context Broker API'
description = 'Get and update collected data of the service chain with topology information.'
version = '0.0.2'

print(f'{title} v{version}')

from elasticsearch_dsl import connections
import falcon
from falcon_auth import FalconAuthMiddleware, BasicAuthBackend
from falcon_marshmallow import Marshmallow
import argparse
import waitress

parser = argparse.ArgumentParser(
    prog='python3 {__FILENAME__}', description=f'{title}: {description}')
parser.add_argument('--port', '-p', type=int,
                    help='TCP Port of the REST Server', default=5000)
parser.add_argument('--es-endpoint', '-e', type=str,
                    help='Elastic Search server hostname/IP:port', default='localhost:9200')
parser.add_argument('--environment', '-n', choices=['production', 'development'],
                    help='Environment mode', default='production')
parser.add_argument('--es-timeout', '-t', type=int,
                    help='Timeout seconds for the connection to Elastic Search', default=20)
parser.add_argument('--version', '-v', help='Show version',
                    action='store_const', const=api.version)
parser.add_argument('--debug', '-d', help='Enable debug', action='store_true')

args = parser.parse_args()


from route import AgentCatalog, AgentInstance, Connection, Data, ExecEnv, ExecEnvType, NetworkLink, NetworkLinkType, Util

api = falcon.API(middleware=[
    FalconAuthMiddleware(BasicAuthBackend(lambda username, password: { 'username': username })),
    Marshmallow()
])

agent_catalog = AgentCatalog()
agent_instance = AgentInstance()
connection = Connection()
data = Data()
exec_env = ExecEnv()
exec_env_type = ExecEnvType()
network_link = NetworkLink()
network_link_type = NetworkLinkType()
util = Util()

api.add_route('/config/catalog', agent_catalog)
api.add_route('/config/instance', agent_instance)
api.add_route('/config/connection', connection)
api.add_route('/data', data)
api.add_route('/config/exec-env', exec_env)
api.add_route('/config/exec-env-type', exec_env_type)
api.add_route('/config/network-link', network_link)
api.add_route('/config/network-link-type', network_link_type)

if args.version is not None:
    print(args.version)
else:
    connections.create_connection(hosts=args.es_endpoint, timeout=args.es_timeout)

    host = '0.0.0.0'
    waitress.serve(api, host=host, port=args.port)
