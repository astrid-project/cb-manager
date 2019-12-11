# cspell:ignore unauth

from app import ns_config as ns
from setup import Setup
from document import Document, InnerDoc
from elasticsearch_dsl import Text, Boolean, Nested
from flask_restplus import fields
from resource import Resource

type_values = ['integer', 'number', 'time-duration',
               'string', 'choice', 'obj', 'boolean', 'binary']


def type_check(data):
    return not data['type'] in ['choice', 'obj'] or 'value' in data


class AgentParameter(InnerDoc):
    LABEL = 'Agent Parameter'

    name = Text()
    type = Text()
    list = Boolean()

    class Index:
        name = 'agent-parameter'

    @staticmethod
    def apply(data):
        if 'list' not in data:
            data['list'] = False


ref = AgentParameter

agent_parameter_model = ns.model(ref.Index.name, {
    'name': fields.String(description='Name', required=True, example='polling'),
    'type': fields.String(description='Parameter type', required=True, enum=type_values, example='time-duration')
}, description='Represent the available parameters for each agent in the catalog', additionalProperties=True)

type_values = ['filename']


class AgentCatalog(Document):
    LABEL = 'Agent in Catalog'

    name = Text()
    parameters = Nested(AgentParameter)

    class Index:
        name = 'agent-catalog'

    @staticmethod
    def get_url():
        return 'agent'


ref = AgentCatalog

model = ns.model(ref.Index.name, {
    'id':  fields.String(description='Unique ID', required=True, example='filebeat'),
    'name': fields.String(description='General name', required=True, example='Filebeat'),
    'parameters': fields.List(fields.Nested(agent_parameter_model), description='List of parameters', required=False),
}, description='Represent the available agent in the catalog', additionalProperties=True)

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
