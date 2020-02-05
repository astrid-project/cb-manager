# cspell:ignore unauth

from elasticsearch_dsl import connections
from flask import Flask
from flask_restplus import Api, Namespace
import logging

title = 'ASTRID Context Broker API'

def es_connection(hosts, timeout):
    connections.create_connection(hosts=hosts, timeout=timeout)


app = Flask(title)
app.es_connection = es_connection
app.config['ERROR_404_HELP'] = False

log = logging.getLogger('ASTRID')
log.setLevel(logging.DEBUG)

ns_catalog = Namespace('catalog', path='/catalog',
                       description='Catalog of available agents')
ns_config = Namespace('config', path='/config',
                      description='Configuration')
ns_data = Namespace('data', path='/data',
                    description='Collected data')
ns_export = Namespace('export', path='/export',
                      description='Export data')
ns_util = Namespace('util', path='/util', description='Utility')

api = Api(app,
          version='0.0.1',
          title=title,
          description='Get and update collected data of the service chain with topology information',
          validate=True,
          format_checker=False,
          ordered=True,
          catch_all_404s=True,
          serve_challenge_on_401=True,
          # TODO: terms_url       =,
          # TODO: contact         =,
          # TODO: license         =,
          # TODO: license_url     =,
          # TODO: endpoint        =,
          # TODO: default         =,
          # TODO: default_label   =,
          # TODO: doc             =,
          # TODO: authorizations  =
          )

api.add_namespace(ns_catalog)
api.add_namespace(ns_config)
api.add_namespace(ns_data)
api.add_namespace(ns_export)
api.add_namespace(ns_util)
