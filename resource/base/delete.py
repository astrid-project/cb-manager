from elasticsearch import RequestError, NotFoundError

from falcon.errors import HTTPBadRequest
from http import HTTPStatus
from reader.query import QueryReader
from utils.sequence import expand


def on_base_delete(self, req, resp, id=None):
    try:
        resp_data = []
        qr = QueryReader(index=self.doc_cls.Index.name)
        s = qr.parse(query=req.context.get('json', {}), id=id) # TODO add YAML and XML support
        for hit in s.execute():
            data = {}
            try:
                obj = self.doc_cls.get(id=hit.meta.id)
                data = dict(id=hit.meta.id)
                obj.delete()
                resp_data_item = dict(status='deleted',
                                      description='{self.doc_name} with the given [id] correctly deleted.',
                                      data=expand(obj.to_dict(), **data), http_status_code=HTTPStatus.OK)
                lcp_handler = self.lcp_handler.get('delete', None)
                if lcp_handler:
                    num_ok, num_errors = lcp_handler(req=hit, resp=resp_data_item)
                resp_data.append(resp_data_item)
            except NotFoundError as not_found_err: # TODO maybe it is useless
                self.log.error(f'Exception: {not_found_err}')
                resp_data.append(dict(status='error', error=True,
                                    description=f'{self.doc_name} with the given [id] not found',
                                    data=data, http_status_code=HTTPStatus.NOT_FOUND))
            except Exception as exception:
                self.log.error(f'Exception: {exception}')
                resp_data.append(dict(status='error', error=True,
                                      description=f'Not possible to delete the {self.doc_name} with the given [id]',
                                      exception=str(exception), data=data,
                                      http_status_code=HTTPStatus.CONFLICT))
        resp.media = resp_data
    except RequestError as req_err:
        raise HTTPBadRequest(title=req_err.error, description=req_err.info)
