from elasticsearch import RequestError
from elasticsearch_dsl import Search, Q

class QueryParser:
    def __init__(self, index):
        self.s = Search(index=index)

    def parse(self, query):
        try:
            self._select(query)
            self._where(query)
            self._order(query)
            self._limit(query)
            res = self.s.execute()
            return [dict(item.to_dict(), id=item.meta.id) for item in res]
        except RequestError as req_error:
            return [] # TODO

    def _select(self, query):
        self.s = self.s.source(query.get('select', None))

    def _where(self, query):
            q = Q()
            for op, filt in query.get('where', []).items():
                prop = filt.get('target', None)
                expr = filt.get('expr', None)
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
                    pass # TODO
            self.s.query = q

    def _order(query):
        for op, order in query.get('order', []).items():
            prop = order.get('target', None)
            mode = order.get('mode', None)

        self.s = self.s.sort()

    def _limit(query):
        limit = query.get('limit', {}):
        start = limit.get('from', 0)
        end = limit.get('to', None)
        if end is None:
            self.s = self.s[start:]
        else:
            self.s = self.s[start, (end + 1)]
