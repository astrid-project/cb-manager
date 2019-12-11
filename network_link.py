# cspell:ignore unauth

from app import ns_config as ns
from setup import Setup
from document import Document
from elasticsearch_dsl import Text
from flask_restplus import fields
from resource import Resource

from network_link_type import NetworkLinkType


class NetworkLink(Document):
    LABEL = 'Network Link'

    type_id = Text()

    class Index:
        name = 'network-link'


ref = NetworkLink

model = ns.model(ref.Index.name, {
    'id':  fields.String(description='Unique ID', required=True, example='network-link-a'),
    'type_id': fields.String(description=f'{NetworkLinkType.LABEL} ID', required=True, example='pnt-to-pnt')
}, description=f'{ref.LABEL} object', additionalProperties=True)

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
