from app import api, ns_catalog
from document import Document
from elasticsearch_dsl import Text
from error import Error
from flask_api import status
from flask_restplus import fields, Resource
from validate import Validate

class AgentCatalog(Document):
    name = Text()

    class Index:
        name = 'agent-catalog'

    @staticmethod
    def get_name():
        return 'Agent in Catalog'

    @staticmethod
    def get_properties():
        return {
            'name': { 'check': Validate.is_name, 'reason': 'Name not valid' }
        }

ref = AgentCatalog.init_with_try()

model = api.model(ref.Index.name, {
    'id':  fields.String(description ='Unique ID', required = True, example = 'filebeat'),
    'name': fields.String(description ='General name', required = True, example = 'Filebeat')
}, description = 'Represent the available agent in the catalog', additionalProperties = True)

@ns_catalog.route('/agent')
@ns_catalog.response(status.HTTP_401_UNAUTHORIZED, 'Unauthorized operation', Error.unauth_op_model)
@ns_catalog.response(status.HTTP_403_FORBIDDEN, 'Authentication required', Error.auth_model)   
class AgentCatalogResource(Resource):
    @ns_catalog.doc(description = f'Get the list of all {ref.get_name()}s')
    @ns_catalog.response(status.HTTP_200_OK, f'List of {ref.get_name()}s', fields.List(fields.Nested(model)))
    def get(self):
        return ref.read_all()

    @ns_catalog.doc(description = f'Add a new {ref.get_name()}')
    @ns_catalog.expect(model, description = f'{ref.get_name()} to add', required = True)
    @ns_catalog.response(status.HTTP_201_CREATED, f'{ref.get_name()} correctly added', Document.response_model)
    @ns_catalog.response(status.HTTP_406_NOT_ACCEPTABLE, 'Request not acceptable', Error.not_acceptable_model)
    @ns_catalog.response(status.HTTP_409_CONFLICT, f'{ref.get_name()} with the same ID already found', Error.found_model)
    def post(self):
        return ref.created()

@ns_catalog.route('/agent-id')
@ns_catalog.response(status.HTTP_401_UNAUTHORIZED, 'Unauthorized operation', Error.unauth_op_model)
@ns_catalog.response(status.HTTP_403_FORBIDDEN, 'Authentication required', Error.auth_model)   
class AgentCatalogResource_id(Resource):
    @ns_catalog.doc(description = f'Get the list of all {ref.get_name()} IDs')
    @ns_catalog.response(status.HTTP_200_OK, f'List of {ref.get_name()} IDs', fields.List(fields.String(description = f'{ref.get_name()} ID', example = 'network-link-a')))
    def get(self):
        return ref.read_all_id()

@ns_catalog.route('/agent/<string:id>')
@ns_catalog.response(status.HTTP_401_UNAUTHORIZED, 'Unauthorized operation', Error.unauth_op_model)
@ns_catalog.response(status.HTTP_403_FORBIDDEN, 'Authentication required', Error.auth_model)
@ns_catalog.response(status.HTTP_404_NOT_FOUND, f'{ref.get_name()} with the given ID not found', Error.found_model)
class AgentCatalogResource_sel(Resource):
    @ns_catalog.doc(description = f'Get the {ref.get_name()} with the given ID')
    @ns_catalog.response(status.HTTP_200_OK, f'{ref.get_name()} with the given ID', model)
    def get(self, id):
        return ref.read(id)

    @ns_catalog.doc(description = f'Update the {ref.get_name()} with the given ID')
    @ns_catalog.response(status.HTTP_202_ACCEPTED, f'{ref.get_name()} with the given ID currectly updated', Document.response_model)
    @ns_catalog.response(status.HTTP_406_NOT_ACCEPTABLE, 'Not acceptable request', Error.not_acceptable_model)
    def put(self, id):
        return ref.updated(id)

    @ns_catalog.doc(description = f'Delete the {ref.get_name()} with the given ID')
    @ns_catalog.response(status.HTTP_202_ACCEPTED, f'{ref.get_name()} with the given ID currectly deleted', Document.response_model)
    def delete(self, id):
        return ref.deleted(id)
