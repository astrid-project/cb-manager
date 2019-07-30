from app import app, api
import argparse
import exec_env
import exec_env_type
import network_link
import network_link_type
import agent_catalog
import agent_instance
import connection
import data

parser = argparse.ArgumentParser(prog = 'python3 context_broker-rest-api.py', description = api.title + ': ' + api.description)
parser.add_argument('--port', '-p', help = 'TCP Port of the REST Server')
parser.add_argument('--version', '-v', help = 'Show version', action = 'store_const', const = api.version)
parser.add_argument('--debug', '-d', help = 'Enable debug', action = 'store_true')

args = parser.parse_args()

if args.version is not None:
    print(args.version)
else:
    app.run(port = args.port, debug = args.debug)