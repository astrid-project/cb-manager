from marshmallow import fields, Schema

class QueryClauseSchema(Schema):


class QuerySchema(Schema):
    select = fields.List(fields.String())
    where = fields.Nested(QueryClauseSchema())
    order = fields.Nested(QueryOrderSchema())