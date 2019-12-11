# cspell:ignore unauth

from app import ns_util as ns
from setup import Setup
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
    # FIXME add model
}, description='DSL Query', additionalProperties=True)

graph_ql_query_model = ns.model('graph-ql-query', {
    # FIXME add model
}, description='GraphQL Query', additionalProperties=True)

sql_query_model = ns.model('sql-query', {
    # FIXME add model
}, description='SQL Query', additionalProperties=True)

setup_dsl = Setup(target=Dsl, namespace=ns, model=dsl_query_model)
setup_graph_ql = Setup(target=GraphQl, namespace=ns,
                       model=graph_ql_query_model)
setup_sql = Setup(target=Sql, namespace=ns, model=sql_query_model)


@setup_dsl.route
@setup_dsl.unauth
@setup_dsl.forbidden
@setup_dsl.headers
class BaseDSL(Resource):
    @setup_dsl.doc
    @setup_dsl.ok
    def get(self):
        pass


@setup_graph_ql.route
@setup_graph_ql.unauth
@setup_graph_ql.forbidden
@setup_graph_ql.headers
class BaseGraphQL(Resource):
    @setup_graph_ql.doc
    @setup_graph_ql.ok
    def get(self):
        pass


@setup_sql.route
@setup_sql.unauth
@setup_sql.forbidden
@setup_sql.headers
class BaseSQL(Resource):
    @setup_sql.doc
    @setup_sql.ok
    def get(self):
        # FIXME: es_sql.execute_sql('http://127.0.0.1:9200', request)
        return None
