from elasticsearch_dsl import Q, Search
from elasticsearch import RequestError
from falcon.errors import HTTPBadRequest
from utils.log import Log


class QueryReader:
    def __init__(self, index):
        self.s = Search(index=index)

    def parse(self, query, id=None):
        try:
            self.__select(query)
            self.s.query = self.__where(query, id=id)
            self.__order(query)
            self.__limit(query)
        except RequestError as req_err:
            raise HTTPBadRequest(title=req_err.error, description=req_err.info)
        except HTTPBadRequest as http_bad_req:
            raise http_bad_req
        except Exception as exception:
            Log.get('query-reader').error(f'Exception: {exception}')
            raise HTTPBadRequest(
                title='Not valid JSON',
                description='The request body is not a valid JSON or it is not encoded as UTF-8.')
        return self.s

    def __select(self, query):
        self.s = self.s.source(query.get('select', None))

    def __where(self, query, id=None):
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
                prop = self.__fix_target(clause.get('target', None))
                expr = clause.get('expr', None)
                if prop is not None and expr is not None:
                    if op == 'equals':
                        q = Q('term', **{prop: expr})
                    elif op == 'reg-exp':
                        q = Q('regexp', **{prop: dict(value=expr)})
                    elif op == 'wildcard':
                        q = Q('wildcard', **{prop: dict(value=expr)})
                    elif op in ['lt', 'lte', 'gt', 'gte']:
                        q = Q('range', **{prop: {op: expr}})
                    else:
                        raise HTTPBadRequest(title='Operation unknown',
                                            description=f'{op} unknown')
                else:
                    raise HTTPBadRequest(title='Request not valid',
                                        description=f'{op} clause with not valid/missing data')
        if id is not None:
            q = q & Q('term', _id=id)
        return q

    def __order(self, query):
        sort_list = []
        for order in query.get('order', []):
            prop = self.__fix_target(order.get('target', None))
            mode = order.get('mode', None)
            if prop is not None and mode is not None:
                sort_list.append(prop if mode == 'asc' else f'-{prop}')
            else:
                raise HTTPBadRequest(title='Request not valid',
                                    description=f'order with not valid/missing data')
        self.s = self.s.sort(*sort_list)

    def __limit(self, query):
        limit = query.get('limit', {})
        start = limit.get('from', None)
        end = limit.get('to', None)
        if end is None:
            if start is not None:
                self.s = self.s[start:]
        else:
            self.s = self.s[start:(end + 1)]

    @staticmethod
    def __fix_target(prop):
        return '_id' if prop == 'id' else prop
