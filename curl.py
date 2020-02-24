import argparse
from configparser import ConfigParser
from requests.auth import HTTPBasicAuth
import json
import requests

config_parser = ConfigParser()
config_parser.read('config.ini')

title = config_parser.get('info', 'title')
description = config_parser.get('info', 'description')
version = config_parser.get('info', 'version')

cb_host = config_parser.get('context-broker', 'host')
cb_port = config_parser.get('context-broker', 'port')

dev_username = config_parser.get('dev', 'username')
dev_password = 'astrid'

timeout = 20
method = 'get'
path = ''
data = ''

parser = argparse.ArgumentParser(
    prog=f'python3 curl.py', description=f'Custom curl for {title} version {version}')

parser.add_argument('--host', '-i', type=str, help='Hostname/IP', default=cb_host)
parser.add_argument('--port', '-o', type=int, help='Port', default=cb_port)

parser.add_argument('--username', '-u', type=str,
                    help='Authorized username', default=dev_username)
parser.add_argument('--password', '-p', type=str,
                    help='Authorized password', default=dev_password)

parser.add_argument('--timeout', '-t', type=float,
                    help='Timeout', default=timeout)
parser.add_argument('--method', '-m', type=str, help='Method', default=method)
parser.add_argument('--path', '-a', type=str, help='Path', default=path)
parser.add_argument('--data', '-d', type=str, help='Request data', default=data)

args = parser.parse_args()

try:
    res = getattr(requests, method)(f'http://{args.ip}:{args.port}/{args.path}',
                       auth=HTTPBasicAuth(args.username, args.password), timeout=args.timeout, json=json.loads(args.data))
except ValueError:
    print(f'Error: not JSON valid data.')
except:
    print(f'Error: connection to {args.ip}:{args.port} not possible.')
else:
    try:
        print(f'Status code: {res.status_code}.')
        print(json.dumps(res.json(), indent=2, sort_keys=True))
    except:
        print('\nError: response with not valid JSON.')
        print(res.content)
