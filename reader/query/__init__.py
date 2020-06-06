from elasticsearch_dsl import Q, Search
from elasticsearch import RequestError
from falcon.errors import HTTPBadRequest
from utils.log import Log


class QueryReader:
    def __init__(self, index):
        self.s = Search(index=index)

    def parse(self, query, id=None):
        try:
            self._select(query)
            self.s.query = self._where(query, id=id)
            self._order(query)
            self._limit(query)
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

    def fix_target(self, prop):
        return '_id' if prop == 'id' else prop

    def _select(self, query):
        self.s = self.s.source(query.get('select', None))

    from reader.query.where import _where
    from reader.query.order import _order
    from reader.query.limit import _limit
