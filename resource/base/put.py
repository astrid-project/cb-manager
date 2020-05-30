from document.nested import edit as nested_edit, rm as nested_rm
from elasticsearch import NotFoundError
from falcon.errors import HTTPBadRequest
from http import HTTPStatus
from utils.sequence import subset, wrap


def on_base_put(self, req, resp, id=None):
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
        if req_data_item_id is None and not single_item:
            resp_data.append(dict(status='error',
                                  reason='Request not valid: id property not found',
                                  http_status_code=HTTPStatus.NOT_FOUND))
        elif req_data_item_id is not None and single_item:
            resp_data.append(dict(status='error',
                                  reason=f'Request not valid: two ids provided',
                                  id=[req_data_item_id, id],
                                  http_status_code=HTTPStatus.CONFLICT))
        else:
            try:
                obj = self.doc_cls.get(id=req_data_item_id)
                if len(req_data_item) == 0:
                    status_item = 'noop'
                else:
                    status_item = 'noop'
                    for nested_field in self.nested_fields:
                        nested_data = wrap(req_data_item.get(nested_field, []))
                        status_item_rm = nested_rm(obj, data=nested_data, field=nested_field)
                        status_item_edit = nested_edit(obj, data=nested_data, field=nested_field)
                        if 'updated' in [status_item_rm, status_item_edit]:
                            status_item = 'updated'
                    subset_req_data_item = subset(req_data_item, *self.nested_fields, negation=True)
                    if len(subset_req_data_item) > 0:
                        status_req_data_item = obj.update(**subset_req_data_item)
                        if status_req_data_item == 'updated':
                            status_item = status_req_data_item
                    resp_data_item = dict(status=status_item,
                                          data=dict(**obj.to_dict(), id=req_data_item_id),
                                          http_status_code=HTTPStatus.OK)
                    resp_data.append(resp_data_item)
                    lcp_handler = self.lcp_handler.get('put', None)
                    if lcp_handler:
                        lcp_handler(req=req_data_item, resp=resp_data_item)
            except NotFoundError as not_found_err:
                self.log.error(f'Exception: {not_found_err}')
                resp_data.append(dict(status='error',
                                      reason=f'{self.doc_name} with the given [id] not found',
                                      id=req_data_item_id,
                                      http_status_code=HTTPStatus.NOT_FOUND))
    resp.media = resp_data
