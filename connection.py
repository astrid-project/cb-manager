from app import api, ns_config
from document import Document
from elasticsearch_dsl import Text
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
            'exec_env_id': { 'check': ExecEnv.exists, 'reason': 'Execution Environment not found' },
            'network_link_id': { 'check': NetworkLink.exists, 'reason': 'Network Link not found' }
        }

ref = Connection.init_with_try()

model = api.model(ref.Index.name, {
    'id':  fields.String(description ='Unique ID', required = True, example = 'connection-1'),
    'exec_env_id': fields.String(description ='Execution Environment ID', required = True, example = 'exec-env-apache'),
    'network_link_id': fields.String(description ='Network Link ID', required = True, example = 'pnt-to-pnt')
}, description = 'Represent the relations between the Execution Environments and the Network Links', additionalProperties = True)


@ns_config.route('/connection')
@ns_config.response(status.HTTP_401_UNAUTHORIZED, 'Unauthorized operation')
@ns_config.response(status.HTTP_403_FORBIDDEN, 'Authentication required')
class ConnetionResource(Resource):
    def get(self):
        return ref.read_all()

    def post(self):
        return ref.created()

@ns_config.route('/connection-id')
@ns_config.response(status.HTTP_401_UNAUTHORIZED, 'Unauthorized operation')
@ns_config.response(status.HTTP_403_FORBIDDEN, 'Authentication required')
class ConnetionResource_id(Resource):
    def get(self):
        return ref.read_all_id()

@ns_config.route('/connection/<string:id>')
@ns_config.response(status.HTTP_401_UNAUTHORIZED, 'Unauthorized operation')
@ns_config.response(status.HTTP_403_FORBIDDEN, 'Authentication required')
class ConnetionResource_sel(Resource):
    def get(self, id):
        return ref.read(id)

    def put(self, id):
        return ref.updated(id)

    def delete(self, id):
        return ref.deleted(id)

@ns_config.route('/connection/exec-env/<string:id>')
@ns_config.response(status.HTTP_401_UNAUTHORIZED, 'Unauthorized operation')
@ns_config.response(status.HTTP_403_FORBIDDEN, 'Authentication required')
class ConnetionResource_by_exec_env(Resource):
    def get(self, id):
        return ref.read_by(exec_env_id = id)

    def delete(self, id):
        return ref.deleted_by(exec_env_id = id)

@ns_config.route('/connection/network_link/<string:id>')
@ns_config.response(status.HTTP_401_UNAUTHORIZED, 'Unauthorized operation')
@ns_config.response(status.HTTP_403_FORBIDDEN, 'Authentication required')
class ConnetionResource_by_network_link(Resource):
    def get(self, id):
        return ref.read_by(network_link_id = id)

    def delete(self, id):
        return ref.deleted_by(network_link_id = id)
