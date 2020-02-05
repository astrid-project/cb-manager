import falcon
from schema import Query
from marshmallow import fields, Schema
import elasticsearch
from elasticsearch_dsl import Document, InnerDoc, Nested, Text, Search, Q


class ExecEnvDocument(Document):
    hostname = Text()
    type_id = Text()

    class Index:
        name = 'exec-env'

ExecEnvDocument.init()

class ExecEnvResource(object, ):
    def on_get(self, req, resp):
        query = req.context['json']
        try:
            s = Search(index=ExecEnvDocument.Index.name)
            if 'select' in query:
                s = s.source(query['select'])
            if 'where' in query:
                q = Q()
                for op, filt in query['where'].items():
                    prop, expr = filt['target'], filt['expr']
                    if op == 'equal':
                        q = Q('term', **{prop: expr})
                    elif op == 'reg-exp':
                        q = Q('regexp', **{prop: dict(value=expr)})
                    elif op == 'wildcard':
                        q = Q('wildcard', **{prop: dict(value=expr)})
                    elif op in ['lt', 'lte', 'gt', 'gte']:
                        q = Q('range', **{prop: {op: expr}})
                s.query = q
            if 'order' in query:
                for op, order in query['order'].items():
                    prop, mode = order['target'], order['mode']

                s = s.sort()
            if 'limit' in query:
                start = query['limit']['from']
                end = query['limit']['from']
                s = s[start, (end + 1)]

            res = s.execute()
            resp.media = [dict(item.to_dict(), id=item.meta.id) for item in res]
        except elasticsearch.RequestError as e:
            pass

    def on_post(self, req, resp):
        pass

    def on_delete(self, req, resp):
        pass

    def on_put(self, req, resp):
        pass
