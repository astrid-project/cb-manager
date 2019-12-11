# cspell:ignore unauth

from app import ns_config as ns
from setup import Setup
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

setup = Setup(target=ref, namespace=ns, model=model)


@setup.route
@setup.unauth
@setup.forbidden
@setup.headers
class Base(Resource):
    @setup.doc
    @setup.input
    @setup.accepted
    @setup.not_found
    def delete(self):
        return ref.deleted()

    @setup.doc
    @setup.input
    @setup.ok
    @setup.not_found
    def get(self):
        return ref.read()

    @setup.doc
    @setup.input
    @setup.created
    @setup.conflict
    def post(self):
        return ref.created()


@setup.route_selected
@setup.unauth
@setup.forbidden
@setup.headers
class Selected(Resource):
    @setup.doc
    @setup.input
    @setup.not_found
    def put(self, id):
        return ref.updated(id)
