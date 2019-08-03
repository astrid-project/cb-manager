from elasticsearch_dsl import connections
from flask import Flask
from flask_restplus import Api, Namespace
import logging

connections.create_connection(hosts = ['localhost'], timeout = 20)

title = 'ASTRID Context Broker API'

app = Flask(title)

app.config['ERROR_404_HELP'] = False

log = logging.getLogger('ASTRID')
log.setLevel(logging.DEBUG)

ns_catalog = Namespace('catalog', path = '/catalog', description = 'Catalog of available agents')
ns_config = Namespace('config', path = '/config', description = 'Configuration')
ns_data = Namespace('data', path = '/data', description = 'Collected data')

api = Api(app,
          version = '0.0.1',
          title = title,
          description = 'Get and update collected data of the service chain with topology information')
        #   terms_url = 'TODO',
        #   contact = 'TODO',
        #   license =  'TODO',
        #   license_url = 'TODO',
        #   endpoint = 'TODO',
        #   default = 'TODO',
        #   default_label =  'TODO',
        #   validate = True,
        #   ordered = True,
        #   doc = 'TODO',
        #   catch_all_404s = True,
        #   authorizations = [],
        #   serve_challenge_on_401 = True,
        #   format_checker = False)

api.add_namespace(ns_catalog)
api.add_namespace(ns_config)
api.add_namespace(ns_data)