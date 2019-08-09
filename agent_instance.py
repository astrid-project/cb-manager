from app import ns_config as ns
from config import Config
from document import Document
from elasticsearch_dsl import Text
from flask_restplus import fields
from resource import Resource

from agent_catalog import AgentCatalog
from exec_env import ExecEnv

status_values = ['start', 'stop']


class AgentInstance(Document):
    LABEL = 'Agent Instance'

    agent_catalog_id = Text()
    exec_env_id = Text()
    status = Text()

    class Index:
        name = 'agent-instance'

    @staticmethod
    def apply(data):
        if 'status' not in data:
            data['status'] = 'stop'


ref = AgentInstance

model = ns.model(ref.Index.name, {
    'id':  fields.String(description='Unique ID', required=True, example='filebeat-apache'),
    'agent_catalog_id': fields.String(description=f'{AgentCatalog.LABEL} ID', required=True, example='filebeat'),
    'exec_env_id': fields.String(description=f'{ExecEnv.LABEL} ID', required=True, example='exec-env-apache'),
    'status': fields.String(description='Status of the agent', required=False, enum=status_values)
}, description=f'Represent the agent instance installed in the {ExecEnv.LABEL}s', additionalProperties=True)

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
