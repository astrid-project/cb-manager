from elasticsearch_dsl import Q
from falcon.errors import HTTPBadRequest


def _where(self, query, id=None):
    q = Q()
    for op, clause in query.get('where', {}).items():
        if op == 'and':
            for sub_op, sub_clause in clause.items():
                q = q & self._where({'where': {sub_op: sub_clause}})
        elif op == 'or':
            for sub_op, sub_clause in clause.items():
                q = q | self._where({'where': {sub_op: sub_clause}})
        elif op == 'not':
            q = ~self._where(clause)
        else:
            prop = self.fix_target(clause.get('target', None))
            expr = clause.get('expr', None)
            if prop is not None and expr is not None:
                if op == 'equals':
                    q = Q('term', **{prop: expr})
                elif op == 'reg-exp':
                    q = Q('regexp', **{prop: dict(value=expr)})
                elif op == 'wildcard':
                    q = Q('wildcard', **{prop: dict(value=expr)})
                elif op in ['lt', 'lte', 'gt', 'gte']:
                    q = Q('range', **{prop: {op: expr}})
                else:
                    raise HTTPBadRequest(title='Operation unknown',
                                         description=f'{op} unknown')
            else:
                raise HTTPBadRequest(title='Request not valid',
                                     description=f'{op} clause with not valid/missing data')
    if id is not None:
        q = q & Q('term', _id=id)
    return q
