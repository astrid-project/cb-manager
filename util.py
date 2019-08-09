from app import ns_util as ns
from config import Config
from document import BaseObject
from elasticsearch_dsl import Text
#import es_sql
from flask_restplus import fields
from resource import Resource


class Dsl(BaseObject):
    LABEL = 'DSL'


class GraphQl(BaseObject):
    LABEL = 'GraphQL'


class Sql(BaseObject):
    LABEL = 'SQL'


dsl_query_model = ns.model('dsl-query', {
    'TODO':  fields.String(description='TODO', required=True)
}, description='DSL Query', additionalProperties=True)

graph_ql_query_model = ns.model('graph-ql-query', {
    'TODO':  fields.String(description='TODO', required=True)
}, description='DSL Query', additionalProperties=True)

sql_query_model = ns.model('sql-query', {
    'TODO':  fields.String(description='TODO', required=True)
}, description='DSL Query', additionalProperties=True)

cnf_dsl = Config(target=Dsl, namespace=ns, model=dsl_query_model)
cnf_graph_ql = Config(target=GraphQl, namespace=ns, model=graph_ql_query_model)
cnf_sql = Config(target=Sql, namespace=ns, model=sql_query_model)


@cnf_dsl.route
@cnf_dsl.unauth
@cnf_dsl.forbidden
@cnf_dsl.headers
class BaseDSL(Resource):
    @cnf_dsl.doc
    @cnf_dsl.ok
    def get(self):
        pass


@cnf_graph_ql.route
@cnf_graph_ql.unauth
@cnf_graph_ql.forbidden
@cnf_graph_ql.headers
class BaseGraphQL(Resource):
    @cnf_graph_ql.doc
    @cnf_graph_ql.ok
    def get(self):
        pass


@cnf_sql.route
@cnf_sql.unauth
@cnf_sql.forbidden
@cnf_sql.headers
class BaseSQL(Resource):
    @cnf_sql.doc
    @cnf_sql.ok
    def get(self):
        return None  # es_sql.execute_sql('http://127.0.0.1:9200', request)
