from app import ns_config as ns
from config import Config
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

cnf = Config(target=ref, namespace=ns, model=model)


@cnf.route
@cnf.unauth
@cnf.forbidden
@cnf.headers
class Base(Resource):
    @cnf.doc
    @cnf.input
    @cnf.accepted
    @cnf.not_found
    def delete(self):
        return ref.deleted()

    @cnf.doc
    @cnf.input
    @cnf.ok
    @cnf.not_found
    def get(self):
        return ref.read()

    @cnf.doc
    @cnf.input
    @cnf.created
    @cnf.conflict
    def post(self):
        return ref.created()


@cnf.route_selected
@cnf.unauth
@cnf.forbidden
@cnf.headers
class Selected(Resource):
    @cnf.doc
    @cnf.input
    @cnf.not_found
    def put(self, id):
        return ref.updated(id)
