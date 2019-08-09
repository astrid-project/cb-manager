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

parser = argparse.ArgumentParser(
    prog='python3 context_broker-rest-api.py', description=api.title + ': ' + api.description)
parser.add_argument('--port', '-p', type=int,
                    help='TCP Port of the REST Server')
parser.add_argument('--es-hosts', '-e', type=str,
                    help='Elastic Search server hostname', default='localhost:9200', action='append')
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
        print(f'Port: {args.port}')
        print(f'ES Hosts: {args.es_hosts}')
        print(f'ES Timeout: {args.es_timeout}s')
    app.es_connection(hosts=args.es_hosts, timeout=args.es_timeout)

    AgentCatalog.setup()
    AgentInstance.setup()
    Connection.setup()
    Data.setup()
    ExecEnv.setup()
    ExecEnvType.setup()
    NetworkLink.setup()
    NetworkLinkType.setup()

    app.run(port=args.port, debug=args.debug)
