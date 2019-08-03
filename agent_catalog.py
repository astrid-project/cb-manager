from app import api, ns_catalog
from document import Document, InnerDoc, Nested
from elasticsearch_dsl import Text, Boolean
from error import Error
from flask_api import status
from flask_restplus import fields, Resource
from validate import Validate

type_values = ['integer', 'number', 'time-duration', 'string', 'choice', 'obj', 'boolean']

def type_check(data):
    return not data['type'] in ['choice', 'obj'] or 'value' in data

class AgentOption(InnerDoc):
    name = Text()
    type = Text()
    list = Boolean()

    class Index:
        name = 'agent-option'

    @staticmethod
    def get_name():
        return 'Agent Option'

    @staticmethod
    def get_properties():
        return { 
            AgentOption.ALL: { 'check': type_check, 'reason': 'Missing value property for this type of data' },
            'name': { 'check': Validate.is_name, 'reason': 'Name not valid', 'required': True },
            'type': { 'check': Validate.is_choice(*type_values), 'reason': f"Type not valid (acceptable values: {', '.join(type_values)})", 'required': True }
        }

    @staticmethod
    def apply(data):
        if 'list' not in data: data['list'] = False

ref = AgentOption.init_with_try()

agent_option_model = api.model(ref.Index.name, {
    'name': fields.String(description ='Name', required = True, example = 'polling'),
    'type': fields.String(decriptione = 'Option type', required = True, enum = type_values, example = 'time-duration')
}, description = 'Represent the available options for each agent in the catalog', additionalProperties = True)

class AgentRecipe(InnerDoc):
    start = Text()
    stop = Text()
    install = Text()
    uninstall = Text()

    class Index:
        name = 'agent-recipe'

    @staticmethod
    def get_name():
        return 'Agent Recipe'

    @staticmethod
    def get_properties():
        return { 
            'start': { 'check': Validate.is_list_unique_type(str), 'reason': 'Start operations not valid', 'required': True },
            'stop': { 'check': Validate.is_list_unique_type(str), 'reason': 'Stop operations not valid', 'required': True },
            'install': { 'check': Validate.is_list_unique_type(str), 'reason': 'Install operations not valid', 'required': True },
            'uninstall': { 'check': Validate.is_list_unique_type(str), 'reason': 'Uninstall operations not valid', 'required': True },
        }

ref = AgentRecipe.init_with_try()

agent_recipe_model = api.model(ref.Index.name, {
    'start': fields.List(fields.String(description ='Start operations', required = True, example = 'TODO')),
    'stop': fields.List(fields.String(decriptione = 'Stop operations', required = True, example = 'TODO')),
    'install': fields.List(fields.String(decriptione = 'Install operations', required = True, example = 'TODO')),
    'uninstall': fields.List(fields.String(decriptione = 'Uninstall operations', required = True, example = 'TODO')),
}, description = 'The recipe with the commands to start, stop, install an uninstall the agent', additionalProperties = True)

class AgentCatalog(Document):
    name = Text()
    options = Nested(AgentOption)
    config = Text()
    recipe = Nested(AgentRecipe)
    
    class Index:
        name = 'agent-catalog'

    @staticmethod
    def get_name():
        return 'Agent in Catalog'

    @staticmethod
    def get_url():
        return 'agent'

    @staticmethod
    def get_properties():
        return {
            'name': { 'check': Validate.is_name, 'reason': 'Name not valid', 'required': True },
            'options': { 'check': Validate.is_list_obj(AgentOption, unique_by = 'name'), 'reason': 'Option list not valid', 'required': False },
            'config': { 'check': Validate.is_str, 'reason': 'Config not valid', 'required': False },
            'recipe': { 'check': Validate.is_obj(AgentRecipe), 'reason': 'Recipe not valid', 'required': True }
        }

ref = AgentCatalog.init_with_try()

model = api.model(ref.Index.name, {
    'id':  fields.String(description ='Unique ID', required = True, example = 'filebeat'),
    'name': fields.String(description ='General name', required = True, example = 'Filebeat'),
    'options': fields.List(fields.Nested(agent_option_model), description = 'List of options', required = False),
    'config': fields.String(description ='Configuration script', required = False, example = 'TODO'),
    'recipe': fields.Nested(agent_recipe_model, description = 'Recipe data', required = True),
}, description = 'Represent the available agent in the catalog', additionalProperties = True)

@ns_catalog.route(f'/{ref.get_url()}')
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

@ns_catalog.route(f'/{ref.get_url()}-id')
@ns_catalog.response(status.HTTP_401_UNAUTHORIZED, 'Unauthorized operation', Error.unauth_op_model)
@ns_catalog.response(status.HTTP_403_FORBIDDEN, 'Authentication required', Error.auth_model)   
class AgentCatalogResource_id(Resource):
    @ns_catalog.doc(description = f'Get the list of all {ref.get_name()} IDs')
    @ns_catalog.response(status.HTTP_200_OK, f'List of {ref.get_name()} IDs', fields.List(fields.String(description = f'{ref.get_name()} ID', example = 'network-link-a')))
    def get(self):
        return ref.read_all_id()

@ns_catalog.route(f'/{ref.get_url()}/{ref.get_id_url()}')
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
