# cspell:ignore unauth

from app import ns_config as ns
from setup import Setup
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
