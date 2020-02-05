title = 'ASTRID Context Broker API'
description = 'Get and update collected data of the service chain with topology information.'
version = '0.0.2'

print(f'{title} v{version}')

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


from route import Code, Config, Status

api = falcon.API(middleware=[
    FalconAuthMiddleware(BasicAuthBackend(lambda username, password: { 'username': username })),
    Marshmallow()
])

status = Status()
code = Code()
config = Config()

api.add_route('/code', code)
api.add_route('/config', config)
api.add_route('/status', status)

if args.version is not None:
    print(args.version)
else:
    host = '0.0.0.0'
    waitress.serve(api, host=host, port=args.port)
