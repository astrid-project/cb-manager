from agent_catalog import AgentCatalog
from app import api, ns_config
from document import Document
from elasticsearch_dsl import Text, Boolean
from exec_env import ExecEnv
from flask import request
from flask_api import status
from flask_restplus import fields, Resource
from validate import Validate

class AgentInstance(Document):
    agent_catalog_id = Text()
    exec_env_id = Text()
    enabled = Boolean()

    class Index:
        name = 'agent-instance'

    @staticmethod
    def get_name():
        return 'Agent instance'

    @staticmethod
    def get_properties():
        return {
            'name': { 'check': Validate.is_name, 'reason': 'Name not valid' },
            'agent_catalog_id': { 'check': AgentCatalog.exists, 'reason': 'Agent not found in the Catalog' },
            'exec_env_id': { 'check': ExecEnv.exists, 'reason': 'Execution Environment not found' },
            'enabled': { 'checl': Validate.is_boolean, 'reason': 'Must be true or false' }
        }

ref = AgentInstance.init_with_try()

model = api.model(ref.Index.name, {
    'id':  fields.String(description ='Unique ID', required = True, example = 'filebeat-apache'),
    'agent_catalog_id': fields.String(description ='Agent Catalog ID', required = True, example = 'filebeat'),
    'exec_env_id': fields.String(description ='Execution Environment ID', required = True, example = 'exec-env-apache'),
    'enabled': fields.Boolean(description ='Indicate if the agent instance is enabled or not', required = True, enum = [True, False])
}, description = 'Represent the agent instance installed in the Execution Environments', additionalProperties = True)

@ns_config.route('/agent')
@ns_config.response(status.HTTP_401_UNAUTHORIZED, 'Unauthorized operation')
@ns_config.response(status.HTTP_403_FORBIDDEN, 'Authentication required')
class AgentInstanceResource(Resource):
    def get(self):
        return ref.read_all()

    def post(self):
        return ref.created()

@ns_config.route('/agent-id')
@ns_config.response(status.HTTP_401_UNAUTHORIZED, 'Unauthorized operation')
@ns_config.response(status.HTTP_403_FORBIDDEN, 'Authentication required')
class AgentInstanceResource_id(Resource):
    def get(self):
        return ref.read_all_id()

@ns_config.route('/agent/<string:id>')
@ns_config.response(status.HTTP_401_UNAUTHORIZED, 'Unauthorized operation')
@ns_config.response(status.HTTP_403_FORBIDDEN, 'Authentication required')
class AgentInstanceResource_sel(Resource):
    def get(self, id):
        return ref.read(id)

    def put(self, id):
        return ref.updated(id)

    def delete(self, id):
        return ref.deleted(id)
