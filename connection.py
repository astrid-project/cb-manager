from app import ns_config as ns
from config import Config
from document import Document
from elasticsearch_dsl import Text
from flask_restplus import fields
from resource import Resource

from exec_env import ExecEnv
from network_link import NetworkLink


class Connection(Document):
    LABEL = 'Connection'

    exec_env_id = Text()
    nextwork_link_id = Text()

    class Index:
        name = 'connection'


ref = Connection

model = ns.model(ref.Index.name, {
    'id':  fields.String(description='Unique ID', required=True, example='connection-1'),
    'exec_env_id': fields.String(description=f'{ExecEnv.LABEL} ID', required=True, example='exec-env-apache'),
    'network_link_id': fields.String(description=f'{NetworkLink.LABEL} ID', required=True, example='pnt-to-pnt')
}, description=f'Represent the relations between the {ExecEnv.LABEL}s and the {NetworkLink.LABEL}s', additionalProperties=True)

cnf = Config(target=ref, namespace=ns, model=model)


@cnf.route
@cnf.unauth
@cnf.forbidden
@cnf.headers
class Base(Resource):
    @cnf.doc
    @cnf.input
    @cnf.accepted
    @cnf.not_found
    def delete(self):
        return ref.deleted()

    @cnf.doc
    @cnf.input
    @cnf.ok
    @cnf.not_found
    def get(self):
        return ref.read()

    @cnf.doc
    @cnf.input
    @cnf.created
    @cnf.conflict
    def post(self):
        return ref.created()


@cnf.route_selected
@cnf.unauth
@cnf.forbidden
@cnf.headers
class Selected(Resource):
    @cnf.doc
    @cnf.input
    @cnf.not_found
    def put(self, id):
        return ref.updated(id)
