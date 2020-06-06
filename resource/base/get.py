from elasticsearch import RequestError
from falcon.errors import HTTPBadRequest
from reader.query import QueryReader


def on_base_get(self, req, resp, id=None):
    try:
        qr = QueryReader(index=self.doc_cls.Index.name)
        # TODO add YAML and XML support
        s = qr.parse(query=req.context.get('json', {}), id=id)
        resp.media = [dict(hit.to_dict(), id=hit.meta.id)
                      for hit in s.execute()]
    except RequestError as req_err:
        raise HTTPBadRequest(title=req_err.error, description=req_err.info)
