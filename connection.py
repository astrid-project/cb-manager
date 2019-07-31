from app import api, ns_config
from document import Document
from elasticsearch_dsl import Text
from error import Error
from exec_env import ExecEnv
from flask import request
from flask_api import status
from flask_restplus import fields, Resource
from network_link import NetworkLink

class Connection(Document):
    exec_env_id = Text()
    nextwork_link_id = Text()

    class Index:
        name = 'connection'

    @staticmethod
    def get_name():
        return 'Connection'

    @staticmethod
    def get_properties():
        return {
            'exec_env_id': { 'check': ExecEnv.exists, 'reason': f'{ExecEnv.get_name()} not found' },
            'network_link_id': { 'check': NetworkLink.exists, 'reason': f'{NetworkLink.get_name()} not found' }
        }

ref = Connection.init_with_try()

model = api.model(ref.Index.name, {
    'id':  fields.String(description ='Unique ID', required = True, example = 'connection-1'),
    'exec_env_id': fields.String(description = f'{ExecEnv.get_name()} ID', required = True, example = 'exec-env-apache'),
    'network_link_id': fields.String(description = f'{NetworkLink.get_name()} ID', required = True, example = 'pnt-to-pnt')
}, description = f'Represent the relations between the {ExecEnv.get_name()}s and the {NetworkLink.get_name()}s', additionalProperties = True)


@ns_config.route(f'/{ref.get_url()}')
@ns_config.response(status.HTTP_401_UNAUTHORIZED, 'Unauthorized operation', Error.unauth_op_model)
@ns_config.response(status.HTTP_403_FORBIDDEN, 'Authentication required', Error.auth_model)
class ConnectionResource(Resource):
    @ns_config.doc(description = f'Get the list of all {ref.get_name()}s')
    @ns_config.response(status.HTTP_200_OK, f'List of {ref.get_name()}s', fields.List(fields.Nested(model)))
    def get(self):
        return ref.read_all()

    @ns_config.doc(description = f'Add a new {ref.get_name()}')
    @ns_config.expect(model, description = f'{ref.get_name()} to add', required = True)
    @ns_config.response(status.HTTP_201_CREATED, f'{ref.get_name()} correctly added', Document.response_model)
    @ns_config.response(status.HTTP_406_NOT_ACCEPTABLE, 'Request not acceptable', Error.not_acceptable_model)
    @ns_config.response(status.HTTP_409_CONFLICT, f'{ref.get_name()} with the same ID already found', Error.found_model)
    def post(self):
        return ref.created()

@ns_config.route(f'/{ref.get_url()}-id')
@ns_config.response(status.HTTP_401_UNAUTHORIZED, 'Unauthorized operation', Error.unauth_op_model)
@ns_config.response(status.HTTP_403_FORBIDDEN, 'Authentication required', Error.auth_model)
class ConnectionResource_id(Resource):
    @ns_config.doc(description = f'Get the list of all {ref.get_name()} IDs')
    @ns_config.response(status.HTTP_200_OK, f'List of {ref.get_name()} IDs', fields.List(fields.String(description = f'{ref.get_name()} ID', example = 'network-link-a')))
    def get(self):
        return ref.read_all_id()

@ns_config.route(f'/{ref.get_url()}/{ref.get_id_url()}')
@ns_config.response(status.HTTP_401_UNAUTHORIZED, 'Unauthorized operation', Error.unauth_op_model)
@ns_config.response(status.HTTP_403_FORBIDDEN, 'Authentication required', Error.auth_model)
@ns_config.response(status.HTTP_404_NOT_FOUND, f'{ref.get_name()} with the given ID not found', Error.found_model)
class ConnectionResource_sel(Resource):
    @ns_config.doc(description = f'Get the {ref.get_name()} with the given ID')
    @ns_config.response(status.HTTP_200_OK, f'{ref.get_name()} with the given ID', model)
    def get(self, id):
        return ref.read(id)

    @ns_config.doc(description = f'Update the {ref.get_name()} with the given ID')
    @ns_config.response(status.HTTP_202_ACCEPTED, f'{ref.get_name()} with the given ID currectly updated', Document.response_model)
    @ns_config.response(status.HTTP_406_NOT_ACCEPTABLE, 'Not acceptable request', Error.not_acceptable_model)
    def put(self, id):
        return ref.updated(id)

    @ns_config.doc(description = f'Delete the {ref.get_name()} with the given ID')
    @ns_config.response(status.HTTP_202_ACCEPTED, f'{ref.get_name()} with the given ID currectly deleted', Document.response_model)
    def delete(self, id):
        return ref.deleted(id)

@ns_config.route(f'/{ref.get_url()}/{ExecEnv.get_url()}/{ExecEnv.get_id_url()}')
@ns_config.response(status.HTTP_401_UNAUTHORIZED, 'Unauthorized operation', Error.unauth_op_model)
@ns_config.response(status.HTTP_403_FORBIDDEN, 'Authentication required', Error.auth_model)
@ns_config.response(status.HTTP_404_NOT_FOUND, f'{ExecEnv.get_name()} with the given ID not found', Error.found_model)
class ConnetionResource_by_exec_env(Resource):
    @ns_config.doc(description = f'Get the list of {ref.get_name()}s of the {ExecEnv.get_name()} with the given ID')
    @ns_config.response(status.HTTP_200_OK, f'List of {ref.get_name()} of the {ExecEnv.get_name()} with the given ID', fields.List(fields.Nested(model)))
    def get(self, id):
        ExecEnv.read(id)
        return ref.read_by(exec_env_id = id)

    @ns_config.doc(description = f'Delete the {ref.get_name()}s of the {ExecEnv.get_name()} with the given ID')
    @ns_config.response(status.HTTP_202_ACCEPTED, f'{ref.get_name()}s of the {ExecEnv.get_name()} with the given ID currectly deleted', Document.response_model)
    def delete(self, id):
        ExecEnv.read(id)
        return ref.deleted_by(exec_env_id = id)

@ns_config.route(f'/{ref.get_url()}/{NetworkLink.get_url()}/{NetworkLink.get_id_url()}')
@ns_config.response(status.HTTP_401_UNAUTHORIZED, 'Unauthorized operation', Error.unauth_op_model)
@ns_config.response(status.HTTP_403_FORBIDDEN, 'Authentication required', Error.auth_model)
@ns_config.response(status.HTTP_404_NOT_FOUND, f'{NetworkLink.get_name()} with the given ID not found', Error.found_model)
class ConnetionResource_by_network_link(Resource):
    @ns_config.doc(description = f'Get the {ref.get_name()} of the {NetworkLink.get_name()} with the given ID')
    @ns_config.response(status.HTTP_200_OK, f'List of {ref.get_name()}s if the {NetworkLink.get_name()} with the given ID', model)
    def get(self, id):
        NetworkLink.read(id)
        return ref.read_by(network_link_id = id)

    @ns_config.doc(description = f'Delete the {ref.get_name()}s of the {NetworkLink.get_name()} with the given ID')
    @ns_config.response(status.HTTP_202_ACCEPTED, f'{ref.get_name()}s of the {NetworkLink.get_name()} with the given ID currectly deleted', Document.response_model)
    def delete(self, id):
        NetworkLink.read(id)
        return ref.deleted_by(network_link_id = id)
