from marshmallow import fields, Schema


class QueryFilterSchema(schema):
    target = fields.String()
    expr = fields.String()


class QueryClauseSchema(Schema):



class QueryOrderSchema(Schema):
    target = fields.String()


class QueryLimitSchema(Schema):
    from = fields.Integer()
    to = fields.Integer()


class QuerySchema(Schema):
    select = fields.List(fields.String())
    where = fields.Nested(QueryClauseSchema())
    order = fields.Nested(QueryOrderSchema())
    limit = fields.Nester(QueryLimitSchema())