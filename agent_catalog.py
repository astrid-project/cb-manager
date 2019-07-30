from app import api, ns_catalog
from document import Document
from elasticsearch_dsl import Text
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
@ns_catalog.response(status.HTTP_401_UNAUTHORIZED, 'Unauthorized operation')
@ns_catalog.response(status.HTTP_403_FORBIDDEN, 'Authentication required')
class AgentCatalogResource(Resource):
    @ns_catalog.response(status.HTTP_200_OK, 'JSON Array of Agents')
    @ns_catalog.marshal_list_with(model)
    def get(self):
        return ref.read_all()

    @ns_catalog.expect(model, validate = True, required = True, description = 'Add a new object')
    @ns_catalog.response(status.HTTP_201_CREATED, 'Agent correctly added')
    @ns_catalog.response(status.HTTP_400_BAD_REQUEST, 'Invalid Syntax')
    def post(self):
        return ref.created()

@ns_catalog.route('/agent-id')
@ns_catalog.response(status.HTTP_401_UNAUTHORIZED, 'Unauthorized operation')
@ns_catalog.response(status.HTTP_403_FORBIDDEN, 'Authentication required')
class AgentCatalogResource_id(Resource):
    @ns_catalog.response(status.HTTP_200_OK, 'JSON Array of Agent IDs')
    def get(self):
        return ref.read_all_id()

@ns_catalog.route('/agent/<string:id>')
@ns_catalog.response(status.HTTP_401_UNAUTHORIZED, 'Unauthorized operation')
@ns_catalog.response(status.HTTP_403_FORBIDDEN, 'Authentication required')
class AgentCatalogResource_sel(Resource):
    @ns_catalog.marshal_with(model)
    def get(self, id):
        return ref.read(id)

    def put(self, id):
        return ref.updated(id)

    def delete(self, id):
        return ref.deleted(id)
