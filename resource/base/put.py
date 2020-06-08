from copy import deepcopy
from document.nested import edit as nested_edit, rm as nested_rm
from elasticsearch import NotFoundError
from falcon.errors import HTTPBadRequest
from http import HTTPStatus
from schema.validate import validate
from utils.sequence import is_list, subset, wrap


def on_base_put(self, req, resp, id=None):
    req_data = req.media
    req_data = validate(schema=self.schema_cls(many=is_list(req_data), unknown='INCLUDE', partial=True),
                        method='PUT', check_unique_id=True, data=req_data, id=id)
    resp_data = []
    for req_data_item in wrap(req_data):
        req_data_item_id = req_data_item.pop('id', None)
        obj = self.doc_cls.get(id=req_data_item_id)
        if len(req_data_item) == 0:
            status_item = 'noop'
        else:
            req_data_lcp = deepcopy(req_data_item)
            self.remove_ignore_fields(req_data_item)
            status_item = 'noop'
            desc_item = 'not'
            for nested_field in self.nested_fields:
                nested_data = wrap(
                    req_data_item.get(nested_field, []))
                status_item_rm = nested_rm(
                    obj, data=nested_data, field=nested_field)
                status_item_edit = nested_edit(
                    obj, data=nested_data, field=nested_field)
                if 'updated' in [status_item_rm, status_item_edit]:
                    status_item = 'updated'
            subset_req_data_item = subset(
                req_data_item, *self.nested_fields, negation=True)
            if len(subset_req_data_item) > 0:
                status_req_data_item = obj.update(
                    **subset_req_data_item)
                if status_req_data_item == 'updated':
                    status_item = status_req_data_item
                if status_item == 'updated':
                    desc_item = 'correctly'
            resp_data_item = dict(data=dict(**obj.to_dict(), id=req_data_item_id),
                                    http_status_code=HTTPStatus.OK)
            lcp_handler = self.lcp_handler.get('put', None)
            if lcp_handler:
                num_ok, num_errors = lcp_handler(
                    instance=obj, req=req_data_lcp, resp=resp_data_item)
                if num_ok > 0:
                    status_item = 'updated'
                    desc_item = 'correctly' if num_errors == 0 else 'partially'
                elif num_errors > 0 and status_item == 'updated':
                    desc_item = 'partially'
            resp_data_item.update(status=status_item,
                                  description=f'{self.doc_name} with the given [id] {desc_item} updated.')
            resp_data.append(resp_data_item)
    resp.media = resp_data
