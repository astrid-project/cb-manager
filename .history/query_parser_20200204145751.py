from elasticsearch import RequestError
from elasticsearch_dsl import Search, Q

class QueryParser:
    def __init__(self, index):
        self.s = Search(index=index)

    def parse(self, query):
        try:
            self._select(query)
            self.s.query = self._where(query)
            self._order(query)
            self._limit(query)
            return [dict(item.to_dict(), id=item.meta.id) for item in self.s.execute()]
        except RequestError as req_error:
            return [] # TODO

    def _select(self, query):
        self.s = self.s.source(query.get('select', None))

    def _where(self, query):
            q = Q()
            for op, filt in query.get('where', []).items():
                if op == 'and':
                    for clause in filt:
                        q = q & self._where(clause)
                elif op == 'or':
                    for clause in filt:
                        q = q | self._where(clause)
                elif op == 'not':
                    q = ~self._where(filt)
                else:
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
            return q

    def _order(self, query):
        sort_list = []
        for order in query.get('order', []):
            prop = order.get('target', None)
            mode = order.get('mode', None)
            if prop is not None and mode is not None:
                sort_list.append(prop if mode == 'asc' else f'-{prop}')
            else:
                pass # TODO
        self.s = self.s.sort(*sort_list) # TODO not work

    def _limit(self, query):
        limit = query.get('limit', {})
        start = limit.get('from', 0)
        end = limit.get('to', None)
        if end is None:
            self.s = self.s[start:]
        else:
            self.s = self.s[start:(end + 1)]
