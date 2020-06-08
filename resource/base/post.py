from copy import deepcopy
from falcon.errors import HTTPBadRequest
from http import HTTPStatus
from marshmallow.exceptions import ValidationError
from schema.validate import validate
from utils.sequence import is_list, wrap


def on_base_post(self, req, resp, id=None):
    req_data = req.media
    req_data = validate(schema=self.schema_cls(many=is_list(req_data), unknown='INCLUDE'),
                        method='POST', check_unique_id=True, data=req_data, id=id)
    resp_data = []
    for req_data_item in wrap(req_data):
        try:
            req_data_lcp = deepcopy(req_data_item)
            req_data_item_id = req_data_item.pop('id')
            self.remove_ignore_fields(req_data_item)
            obj = self.doc_cls(meta=dict(id=req_data_item_id), **req_data_item)
            obj.save()
            resp_data_item = dict(status='created',
                                  description=f'{self.doc_name} with the given [id] correctly created.',
                                  data=dict(id=obj.meta.id, **obj.to_dict()),
                                  http_status_code=HTTPStatus.CREATED)
            resp_data.append(resp_data_item)
            lcp_handler = self.lcp_handler.get('post', None)
            if lcp_handler:
                num_ok, num_errors = lcp_handler(
                    instance=obj, req=req_data_lcp, resp=resp_data_item)
        except Exception as exception:
            self.log.error(f'Exception: {exception}')
            resp_data.append(dict(status='error', error=True, exception=str(exception),
                                  description=f'Not possible to create a {self.doc_name} with the given [data]',
                                  data=dict(id=req_data_item_id, **req_data_item),
                                  http_status_code=HTTPStatus.UNPROCESSABLE_ENTITY))
    resp.media = resp_data
