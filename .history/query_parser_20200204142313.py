from elasticsearch_dsl import Search, Q

class QueryParser:
    def __init__(self, index, query):
        self.s = Search(index=index)
        self._select(query)
        self._where(query)
        self._order(query)
        self._limit(query)

    def _select(query):
        if 'select' in query:
            self.s = self.s.source(query['select'])

    def where(query):
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
                start = query['limit'].get('from', 0)
                end = query['limit'].get('to', None)
                if end is None:
                    s = s = s[start:]
                else:
                    s = s[start, (end + 1)]
