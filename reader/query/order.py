from falcon.errors import HTTPBadRequest


def _order(self, query):
    sort_list = []
    for order in query.get('order', []):
        prop = self.fix_target(order.get('target', None))
        mode = order.get('mode', None)
        if prop is not None and mode is not None:
            sort_list.append(prop if mode == 'asc' else f'-{prop}')
        else: raise HTTPBadRequest(title='Request not valid',
                                   description=f'order with not valid/missing data')
    self.s = self.s.sort(*sort_list)
