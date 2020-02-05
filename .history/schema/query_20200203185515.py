from marshmallow import fields, Schema

class QuerySchema(Schema):
    select = fields.List(fields.String())