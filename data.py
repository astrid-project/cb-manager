from agent_catalog import AgentCatalog
from agent_instance import AgentInstance
from app import api, ns_data
from document import Document
from elasticsearch_dsl import Text, Date
from error import Error
from exec_env import ExecEnv
from flask import request
from flask_api import status
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
            'exec_env_id': { 'check': ExecEnv.exists, 'reason': f'{ExecEnv.get_name()} not found' },
            'agent_instance_id': { 'check': AgentInstance.exists, 'reason': f'{AgentInstance.get_name()} not found' },
            'timestamp_event': { 'check': Validate.is_datetime, 'reason': 'Date/Time not valid' },
            'timestamp_agent': { 'check': Validate.is_datetime, 'reason': 'Date/Time not valid' }
        }

    @staticmethod
    def apply(data):
        data['agent_catalog_id'] = AgentInstance.get_by_id(data['agent_instance_id']).agent_catalog_id

ref = Data.init_with_try()

model = api.model(ref.Index.name, {
    'id':  fields.String(description ='Unique ID', required = True, example = 'filebeat-apache'),
    'exec_env_id': fields.String(description = f'{ExecEnv.get_name()} ID', required = True, example = 'exec-env-apache'),
    'agent_instance_id': fields.String(description = f'{AgentInstance.get_name()} ID', required = True, example = 'filebeat-apache'),
    'agent_catalog_id': fields.String(description = f'{AgentCatalog.get_name()} ID', example = 'filebeat'),
    'timestamp_event': fields.DateTime(description ='Timestamp of the event in the collected data', required = True),
    'timestamp_agent': fields.DateTime(description ='Timestamp when the agent instance collected the data', required = True)
}, description = 'Represent the collected data', additionalProperties = True)

@ns_data.route('/')
@ns_data.response(status.HTTP_401_UNAUTHORIZED, 'Unauthorized operation', Error.unauth_op_model)
@ns_data.response(status.HTTP_403_FORBIDDEN, 'Authentication required', Error.auth_model)
class DataResource(Resource):
    @ns_data.doc(description = f'Get the list of all {ref.get_name()}')
    @ns_data.response(status.HTTP_200_OK, f'List of {ref.get_name()}', fields.List(fields.Nested(model)))
    def get(self, id):
        return ref.read_all()

@ns_data.route('/exec-env/<string:id>')
@ns_data.response(status.HTTP_401_UNAUTHORIZED, 'Unauthorized operation', Error.unauth_op_model)
@ns_data.response(status.HTTP_403_FORBIDDEN, 'Authentication required', Error.auth_model)
@ns_data.response(status.HTTP_404_NOT_FOUND, f'{ExecEnv.get_name()} with the given ID not found', Error.found_model)
class DataResource_by_exec_env(Resource):
    @ns_data.doc(description = f'Get the list of all {ref.get_name()} related to the {ExecEnv.get_name()} with the given ID')
    @ns_data.response(status.HTTP_200_OK, f'List of {ref.get_name()} related to the {ExecEnv.get_name()} with the given ID', fields.List(fields.Nested(model)))
    def get(self, id):
        return ref.read_by(exec_env_id = id)

@ns_data.route('/agent/instance/<string:id>')
@ns_data.response(status.HTTP_401_UNAUTHORIZED, 'Unauthorized operation', Error.unauth_op_model)
@ns_data.response(status.HTTP_403_FORBIDDEN, 'Authentication required', Error.auth_model)
@ns_data.response(status.HTTP_404_NOT_FOUND, f'{AgentInstance.get_name()} with the given ID not found', Error.found_model)
class DataResource_by_agent_instance(Resource):
    @ns_data.doc(description = f'Get the list of all {ref.get_name()} related to the {AgentInstance.get_name()} with the given ID')
    @ns_data.response(status.HTTP_200_OK, f'List of {ref.get_name()} related to the {AgentInstance.get_name()} with the given ID', fields.List(fields.Nested(model)))
    def get(self, id):
        return ref.read_by(agent_instance_id = id)

@ns_data.route('/agent/catalog/<string:id>')
@ns_data.response(status.HTTP_401_UNAUTHORIZED, 'Unauthorized operation', Error.unauth_op_model)
@ns_data.response(status.HTTP_403_FORBIDDEN, 'Authentication required', Error.auth_model)
@ns_data.response(status.HTTP_404_NOT_FOUND, f'{AgentCatalog.get_name()} with the given ID not found', Error.found_model)
class DataResource_by_agent_catalog(Resource):
    @ns_data.doc(description = f'Get the list of all {ref.get_name()} related to the {AgentCatalog.get_name()} with the given ID')
    @ns_data.response(status.HTTP_200_OK, f'List of {ref.get_name()} related to the {AgentCatalog.get_name()} with the given ID', fields.List(fields.Nested(model)))
    def get(self, id):
        return ref.read_by(agent_catalog_id = id)

@ns_data.route('/timestamp/event/after/<string:after>')
@ns_data.response(status.HTTP_401_UNAUTHORIZED, 'Unauthorized operation', Error.unauth_op_model)
@ns_data.response(status.HTTP_403_FORBIDDEN, 'Authentication required', Error.auth_model)
class DataResource_by_timestamp_event_after(Resource):
    @ns_data.doc(description = f'Get the list of all {ref.get_name()} with the event occured after the given parameter')
    @ns_data.response(status.HTTP_200_OK, f'List of {ref.get_name()} with the event occured after the given parameter', fields.List(fields.Nested(model)))
    def get(self, after):
        return ref.read_by_datetime(property = 'timestamp_event', after = after)

@ns_data.route('/timestamp/event/before/<string:before>')
@ns_data.response(status.HTTP_401_UNAUTHORIZED, 'Unauthorized operation', Error.unauth_op_model)
@ns_data.response(status.HTTP_403_FORBIDDEN, 'Authentication required', Error.auth_model)
class DataResource_by_timestamp_event_before(Resource):
    @ns_data.doc(description = f'Get the list of all {ref.get_name()} with the event occured before the given parameter')
    @ns_data.response(status.HTTP_200_OK, f'List of {ref.get_name()} with the event occured before the given parameter', fields.List(fields.Nested(model)))
    def get(self, before):
        return ref.read_by_datetime(property = 'timestamp_event', before = before)

@ns_data.route('/timestamp/event/<string:after>/<string:before>')
@ns_data.response(status.HTTP_401_UNAUTHORIZED, 'Unauthorized operation', Error.unauth_op_model)
@ns_data.response(status.HTTP_403_FORBIDDEN, 'Authentication required', Error.auth_model)
class DataResource_by_timestamp_event(Resource):
    @ns_data.doc(description = f'Get the list of all {ref.get_name()} with the event occured after and before the given parameters')
    @ns_data.response(status.HTTP_200_OK, f'List of {ref.get_name()} with the event occured after and before the given parameters', fields.List(fields.Nested(model)))
    def get(self, after, before):
        return ref.read_by_datetime(property = 'timestamp_event', after = after, before = before)

@ns_data.route('/timestamp/agent/after/<string:after>')
@ns_data.response(status.HTTP_401_UNAUTHORIZED, 'Unauthorized operation', Error.unauth_op_model)
@ns_data.response(status.HTTP_403_FORBIDDEN, 'Authentication required', Error.auth_model)
class DataResource_by_timestamp_agent_after(Resource):
    @ns_data.doc(description = f'Get the list of all {ref.get_name()} collected by the agent after the given parameter')
    @ns_data.response(status.HTTP_200_OK, f'List of {ref.get_name()} collected by the agent after the given parameter', fields.List(fields.Nested(model)))
    def get(self, after):
        return ref.read_by_datetime(property = 'timestamp_agent', after = after)

@ns_data.route('/timestamp/agent/before/<string:before>')
@ns_data.response(status.HTTP_401_UNAUTHORIZED, 'Unauthorized operation', Error.unauth_op_model)
@ns_data.response(status.HTTP_403_FORBIDDEN, 'Authentication required', Error.auth_model)
class DataResource_by_timestamp_agent_before(Resource):
    @ns_data.doc(description = f'Get the list of all {ref.get_name()} collected by the agent before the given parameter')
    @ns_data.response(status.HTTP_200_OK, f'List of {ref.get_name()} collected by the agent before the given parameter', fields.List(fields.Nested(model)))
    def get(self, before):
        return ref.read_by_datetime(property = 'timestamp_agent', before = before)

@ns_data.route('/timestamp/agent/<string:after>/<string:before>', doc = {'params': {'after': 'after', 'before': 'before'}})
@ns_data.response(status.HTTP_401_UNAUTHORIZED, 'Unauthorized operation', Error.unauth_op_model)
@ns_data.response(status.HTTP_403_FORBIDDEN, 'Authentication required', Error.auth_model)
class DataResource_by_timestamp_agent(Resource):
    @ns_data.doc(description = f'Get the list of all {ref.get_name()} collected by the agent before and after the given parameters')
    @ns_data.response(status.HTTP_200_OK, f'List of {ref.get_name()} collected by the agent before and after the given parameters', fields.List(fields.Nested(model)))
    def get(self, after, before):
        return ref.read_by_datetime(property = 'timestamp_agent', after = after, before = before)
