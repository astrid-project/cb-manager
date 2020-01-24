# cspell:ignore reloader

from app import app, api
import argparse
from agent_catalog import AgentCatalog
from agent_instance import AgentInstance
from connection import Connection
from data import Data
from exec_env import ExecEnv
from exec_env_type import ExecEnvType
from network_link import NetworkLink
from network_link_type import NetworkLinkType
import postman
import util
import waitress

parser = argparse.ArgumentParser(
    prog='python3 context_broker-rest-api.py', description=api.title + ': ' + api.description)
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

if args.version is not None:
    print(args.version)
else:
    if args.debug:
        if args.environment == 'production':
            print(
                'Debug mode not work in production environment. Use development instead.')
        print(f'Port: {args.port}')
        print(f'ES Endpoint: {args.es_endpoint}')
        print(f'ES Timeout: {args.es_timeout}s')
    app.es_connection(hosts=args.es_endpoint, timeout=args.es_timeout)

    AgentCatalog.setup()
    AgentInstance.setup()
    Connection.setup()
    Data.setup()
    ExecEnv.setup()
    ExecEnvType.setup()
    NetworkLink.setup()
    NetworkLinkType.setup()

    host = '0.0.0.0'

    if args.environment == 'production':
        waitress.serve(app, host=host, port=5000)
    else:
        app.run(host=host, port=args.port,
                debug=args.debug, use_reloader=False)
