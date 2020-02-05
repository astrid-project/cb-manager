from elasticsearch_dsl import Search, Q

class QueryParser:
    def __init__(self, index, query):
        self.s = Search(index=index)
        self._select(query)
        self._where(query)
        self._order(query)
        self._limit(query)

    def _select(self, query):
        if 'select' in query:
            self.s = self.s.source(query['select'])

    def _where(self, query):
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
            self.s.query = q

    def _order(query):
        if 'order' in query:
            for op, order in query['order'].items():
                prop = order.get('target', None)
                mode = order.get('mode', None)

            self.s = self.s.sort()

    def _limit(query):
        if 'limit' in query:
            start = query['limit'].get('from', 0)
            end = query['limit'].get('to', None)
            if end is None:
                self.s = self.s[start:]
            else:
                self.s = self.s[start, (end + 1)]
