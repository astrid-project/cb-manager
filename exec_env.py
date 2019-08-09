from app import ns_config as ns
from config import Config
from document import Document
from elasticsearch_dsl import Text
from flask_restplus import fields
from resource import Resource

from elasticsearch import RequestError

from exec_env_type import ExecEnvType


class ExecEnv(Document):
    LABEL = 'Execution Environment'

    hostname = Text()
    type_id = Text()

    class Index:
        name = 'exec-env'


ref = ExecEnv

model = ns.model(ref.Index.name, {
    'id':  fields.String(description='Unique ID', required=True, example='exec-env-apache'),
    'hostname': fields.String(description=f'Hostname where the {ref.LABEL} is allocated', required=True, example='host.domain.com'),
    'type_id': fields.String(description=f'{ExecEnvType.LABEL} ID', required=True, example='vm')
}, description=f'{ref.LABEL} object', additionalProperties=True)

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
