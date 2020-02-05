from marshmallow import fields, Schema


class QueryFilterSchema(schema):
    target = fields.String()
    expr = fields.String()


class QueryClauseSchema(Schema):
    and = fields.List(fields.Nested(QueryClauseSchema))
    or = fields.List(fields.Nested(QueryClauseSchema))
    not = fields.List(fields.Nested(QueryClauseSchema))
    lte = fields.Nested(QueryClauseSchema)
    gte = fields.Nested(QueryClauseSchema)
    lt = fields.Nested(QueryClauseSchema)
    gt = fields.Nested(QueryClauseSchema)
    equal = fields.Nested(QueryClauseSchema)
    req_exp = fields.Nested(QueryClauseSchema)

class QueryOrderSchema(Schema):
    target = fields.String()
    mode = fields.String(enum=['asc', 'desc'])


class QueryLimitSchema(Schema):
    from = fields.Integer()
    to = fields.Integer()


class QuerySchema(Schema):
    select = fields.List(fields.String())
    where = fields.Nested(QueryClauseSchema())
    order = fields.Nested(QueryOrderSchema())
    limit = fields.Nester(QueryLimitSchema())