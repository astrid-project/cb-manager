from falcon.errors import HTTPBadRequest
from http import HTTPStatus
from utils.sequence import wrap


def on_base_post(self, req, resp, id=None, lcp_handler=None):
    resp_data = []
    req_data = req.context.get('json', [])
    if id is not None:
        if type(req_data) is list:
            raise HTTPBadRequest(title='id provided',
                                 description=f'Request can create only 1 new {self.doc_name}')
        single_item = True
    else:
        single_item = False
    for req_data_item in wrap(req_data):
        req_data_item_id = req_data_item.pop('id', None)
        if req_data_item_id is not None and single_item:
            resp_data.append(dict(status='error',
                                  reason=f'Request not valid: two ids provided',
                                  id=[req_data_item_id, id],
                                  http_status_code=HTTPStatus.CONFLICT))
        else:
            try:
                if req_data_item_id is not None:
                    obj = self.doc_cls.get(id=req_data_item_id, ignore=404)
                    meta = dict(id=req_data_item_id)
                else:
                    obj = None
                    meta = {}
                if obj is None:
                    obj = self.doc_cls(meta=meta, **req_data_item)
                    status_item = obj.save()
                    resp_data_item = dict(status=status_item,
                                          data=dict(id=obj.meta.id, **obj.to_dict()),
                                          http_status_code=HTTPStatus.CREATED)
                    resp_data.append(resp_data_item)
                    lcp_handler = self.lcp_handler.get('post', None)
                    if lcp_handler:
                        lcp_handler(req=req_data_item, resp=resp_data_item)
                else:
                    resp_data.append(dict(status='error',
                                          reason=f'{self.doc_name} with the given [id] already found',
                                          od=obj.meta.id, http_status_code=HTTPStatus.CONFLICT))
            except Exception as exception:
                self.log.error(f'Exception: {exception}')
                resp_data.append(dict(status='error',
                                      reason=f'Not possible create {self.doc_name} with the given [data]',
                                      data=dict(id=id, **req_data_item),
                                      http_status_code=HTTPStatus.UNPROCESSABLE_ENTITY))
    resp.media = resp_data
