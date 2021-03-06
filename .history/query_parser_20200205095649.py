import falcon
import elasticsearch
from elasticsearch_dsl import Search, Q
from utils import fix_target

class QueryParser:
    def __init__(self, index):
        self.s = Search(index=index)

    def parse(self, query, id=None):
        try:
            self._select(query)
            self.s.query = self._where(query, id=id)
            self._order(query)
            self._limit(query)
        except elasticsearch.RequestError as req_error:
            raise falcon.HTTPBadRequest(
                title=req_error.error, description=req_error.info)
        return self.s

    def _select(self, query):
        self.s = self.s.source(query.get('select', None))

    def _where(self, query, id=None):
        q = Q()
        for op, clause in query.get('where', {}).items():
            if op == 'and':
                for sub_op, sub_clause in clause.items():
                    q = q & self._where({'where': {sub_op: sub_clause}})
            elif op == 'or':
                for sub_op, sub_clause in clause.items():
                    q = q | self._where({'where': {sub_op: sub_clause}})
            elif op == 'not':
                q = ~self._where(clause)
            else:
                prop = fix_target(clause.get('target', None))
                expr = clause.get('expr', None)
                if prop is not None and expr is not None:
                    if op == 'equal':
                        q = Q('term', **{prop: expr})
                    elif op == 'reg-exp':
                        q = Q('regexp', **{prop: dict(value=expr)})
                    elif op == 'wildcard':
                        q = Q('wildcard', **{prop: dict(value=expr)})
                    elif op in ['lt', 'lte', 'gt', 'gte']:
                        q = Q('range', **{prop: {op: expr}})
                else:
                    raise falcon.HTTPBadRequest(
                        title='Request not valid', description=f'{op} clause with not valid/missing data')
        if id is not None:
            q = q & Q('match', _id=id)
        return q

    def _order(self, query):
        sort_list = []
        for order in query.get('order', []):
            prop = fix_target(order.get('target', None))
            mode = order.get('mode', None)
            if prop is not None and mode is not None:
                sort_list.append(prop if mode == 'asc' else f'-{prop}')
            else:
                raise falcon.HTTPBadRequest(
                    title='Request not valid', description=f'order with not valid/missing data')
        self.s = self.s.sort(*sort_list)

    def _limit(self, query):
        limit = query.get('limit', {})
        start = limit.get('from', None)
        end = limit.get('to', None)
        if end is None:
            if start is not None:
                self.s = self.s[start:]
        else:
            self.s = self.s[start:(end + 1)]
