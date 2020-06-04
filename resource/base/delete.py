from elasticsearch import RequestError
from falcon.errors import HTTPBadRequest
from http import HTTPStatus
from reader.query import QueryReader
from utils.sequence import expand


def on_base_delete(self, req, resp, id=None):
    try:
        resp_data = []
        qr = QueryReader(index=self.doc_cls.Index.name)
        s = qr.parse(query=req.context.get('json', {}), id=id)
        for hit in s.execute():
            data = {}
            try:
                obj = self.doc_cls.get(id=hit.meta.id)
                data = obj.to_dict()
                obj.delete()
                resp_data_item = dict(status='deleted',
                                      description='{self.doc_name} with the given [id] correctly deleted.',
                                      data=expand(data, id=hit.meta.id), http_status_code=HTTPStatus.OK)
                lcp_handler = self.lcp_handler.get('delete', None)
                if lcp_handler:
                    lcp_handler(req=hit, resp=resp_data_item)
                resp_data.append(resp_data_item)
            except Exception as exception:
                self.log.error(f'Exception: {exception}')
                resp_data.append(dict(status='error', error=True,
                                      description='Not possible to delete element with the given [id]',
                                      exception=str(exception), data=expand(data, id=hit.meta.id),
                                      http_status_code=HTTPStatus.CONFLICT))
        resp.media = resp_data
    except RequestError as req_err:
        raise HTTPBadRequest(title=req_err.error, description=req_err.info)
