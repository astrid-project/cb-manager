from app import ns_data as ns
from config import Config
from document import Document
from elasticsearch_dsl import Text, Date
from flask_restplus import fields
from resource import Resource

from agent_catalog import AgentCatalog
from agent_instance import AgentInstance
from exec_env import ExecEnv


class Data(Document):
    LABEL = 'Data'

    exec_env_id = Text()
    agent_instance_id = Text()
    timestamp_event = Date()
    timestamp_agent = Date()

    class Index:
        name = 'data'

    @staticmethod
    def apply(data):
        data['agent_catalog_id'] = AgentInstance.get_by_id(
            data['agent_instance_id']).agent_catalog_id


ref = Data

model = ns.model(ref.Index.name, {
    'id':  fields.String(description='Unique ID', required=True, example='filebeat-apache'),
    'exec_env_id': fields.String(description=f'{ExecEnv.LABEL} ID', required=True, example='exec-env-apache'),
    'agent_instance_id': fields.String(description=f'{AgentInstance.LABEL} ID', required=True, example='filebeat-apache'),
    'agent_catalog_id': fields.String(description=f'{AgentCatalog.LABEL} ID', example='filebeat'),
    'timestamp_event': fields.DateTime(description='Timestamp of the event in the collected data', required=True),
    'timestamp_agent': fields.DateTime(description='Timestamp when the agent instance collected the data', required=True)
}, description='Represent the collected data', additionalProperties=True)


cnf = Config(target=ref, namespace=ns, model=model)


@cnf.route_root
@cnf.unauth
@cnf.forbidden
@cnf.headers
class Base(Resource):
    @cnf.doc
    @cnf.ok
    @cnf.not_acceptable
    def get(self):
        return ref.read()
