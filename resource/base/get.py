from elasticsearch import RequestError
from falcon.errors import HTTPBadRequest
from reader.query import QueryReader
from schema.query_request import QueryRequestSchema
from schema.validate import validate

from schema.agent.instance import AgentInstanceSchema

def on_base_get(self, req, resp, id=None):
    req_data = validate(schema=QueryRequestSchema(), method='GET', data=req.media)
    resp_data = []
    try:
        qr = QueryReader(index=self.doc_cls.Index.name)
        s = qr.parse(query=req_data, id=id)
        resp_data = [dict(hit.to_dict(), id=hit.meta.id) for hit in s.execute()]
        resp.media = validate(schema=self.schema_cls(many=True, unknown='INCLUDE'), method='GET', data=resp_data)
    except RequestError as req_err:
        raise HTTPBadRequest(title=req_err.error, description=req_err.info)
