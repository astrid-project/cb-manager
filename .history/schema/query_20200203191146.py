from marshmallow import fields, Schema


class QueryFilterSchema(Schema):
    target = fields.String()
    expr = fields.String()


class QueryClauseSchema(Schema):
    _and = fields.List(fields.Nested(lambda: QueryClauseSchema()), data_key='and')
    _or = fields.List(fields.Nested(lambda: QueryClauseSchema), data_key='or')
    _not = fields.List(fields.Nested(lambda: QueryClauseSchema), data_key='not')
    lte = fields.Nested(QueryFilterSchema)
    gte = fields.Nested(QueryFilterSchema)
    lt = fields.Nested(QueryFilterSchema)
    gt = fields.Nested(QueryFilterSchema)
    equal = fields.Nested(QueryFilterSchema)
    reg_exp = fields.Nested(QueryFilterSchema, data_key='reg-exp')


class QueryOrderSchema(Schema):
    target = fields.String()
    mode = fields.String(enum=['asc', 'desc'])


class QueryLimitSchema(Schema):
    _from = fields.Integer(data_key='from')
    _to = fields.Integer(data_key='to')


class QuerySchema(Schema):
    select = fields.List(fields.String())
    where = fields.Nested(QueryClauseSchema())
    order = fields.Nested(QueryOrderSchema())
    limit = fields.Nester(QueryLimitSchema())
