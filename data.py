from agent_instance import AgentInstance
from app import api, ns_data
from document import Document
from elasticsearch_dsl import Text, Date
from exec_env import ExecEnv
from flask import request
from flask_restplus import fields, Resource
from validate import Validate

class Data(Document):
    exec_env_id = Text()
    agent_instance_id = Text()
    timestamp_event = Date()
    timestamp_agent = Date()

    class Index:
        name = 'data'

    @staticmethod
    def get_name():
        return 'Data'

    @staticmethod
    def get_properties():
        return {
            'exec_env_id': { 'check': ExecEnv.exists, 'reason': 'Execution Environment not found' },
            'agent_instance_id': { 'check': AgentInstance.exists, 'reason': 'Agent instance not found' },
            'timestamp_event': { 'check': Validate.is_datetime, 'reason': 'Date/Time not valid' },
            'timestamp_agent': { 'check': Validate.is_datetime, 'reason': 'Date/Time not valid' }
        }

    @staticmethod
    def apply(data):
        data['agent_catalog_id'] = AgentInstance.get_by_id(data['agent_instance_id']).agent_catalog_id

ref = Data.init_with_try()

model = api.model(ref.Index.name, {
    'id':  fields.String(description ='Unique ID', required = True, example = 'filebeat-apache'),
    'exec_env_id': fields.String(description ='Execution Environment ID', required = True, example = 'exec-env-apache'),
    'agent_instance_id': fields.String(description ='Agent Instance ID', required = True, example = 'filebeat-apache'),
    'agent_catalog_id': fields.String(description ='Agent Catalog ID', required = True, example = 'filebeat'),
    'timestamp_event': fields.DateTime(description ='Timestamp of the event in the collected data', required = True, example = '2015-01-01T12:10:30Z'),
    'timestamp_agent': fields.DateTime(description ='Timestamp when the Agent collected the data', required = True, example = '2015-01-01T12:10:30Z')
}, description = 'Represent the collected data', additionalProperties = True)

@ns_data.route('/')
class DataResource(Resource):
    def get(self, id):
        return ref.read_all()

@ns_data.route('/exec-env/<string:id>')
class DataResource_by_exec_env(Resource):
    def get(self, id):
        return ref.read_by(exec_env_id = id)

@ns_data.route('/agent/instance/<string:id>')
class DataResource_by_agent_instance(Resource):
    def get(self, id):
        return ref.read_by(agent_instance_id = id)

@ns_data.route('/agent/catalog/<string:id>')
class DataResource_by_agent_catalog(Resource):
    def get(self, id):
        return ref.read_by(agent_catalog_id = id)

@ns_data.route('/timestamp/event/after/<string:after>')
class DataResource_by_timestamp_event_after(Resource):
    def get(self, after):
        return ref.read_by_datetime(property = 'timestamp_event', after = after)

@ns_data.route('/timestamp/event/before/<string:before>')
class DataResource_by_timestamp_event_before(Resource):
    def get(self, before):
        return ref.read_by_datetime(property = 'timestamp_event', before = before)

@ns_data.route('/timestamp/event/<string:after>/<string:before>')
class DataResource_by_timestamp_event(Resource):
    def get(self, after, before):
        return ref.read_by_datetime(property = 'timestamp_event', after = after, before = before)

@ns_data.route('/timestamp/agent/after/<string:after>')
class DataResource_by_timestamp_agent_after(Resource):
    def get(self, after):
        return ref.read_by_datetime(property = 'timestamp_agent', after = after)

@ns_data.route('/timestamp/agent/before/<string:before>')
class DataResource_by_timestamp_agent_before(Resource):
    def get(self, before):
        return ref.read_by_datetime(property = 'timestamp_agent', before = before)

@ns_data.route('/timestamp/agent/<string:after>/<string:before>')
class DataResource_by_timestamp_agent(Resource):
    def get(self, after, before):
        return ref.read_by_datetime(property = 'timestamp_agent', after = after, before = before)
