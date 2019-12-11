# cspell:ignore unauth

from app import ns_config as ns
from setup import Setup
from document import Document
from elasticsearch_dsl import Text
from flask_restplus import fields
from resource import Resource


class ExecEnvType(Document):
    LABEL = 'Execution Environment Type'

    name = Text()

    class Index:
        name = 'exec-env-type'


ref = ExecEnvType

model = ns.model(ref.Index.name, {
    'id':  fields.String(description='Unique ID', required=True, example='vm'),
    'name': fields.String(description='General name', required=True, example='Virtual Machine')
}, description=f'{ref.LABEL} object', additionalProperties=True)

setup = Setup(target=ref, namespace=ns, model=model)


@setup.route
@setup.unauth
@setup.forbidden
@setup.headers
class Resource(Resource):
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
