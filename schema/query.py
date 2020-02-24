from marshmallow import fields, Schema


class QueryRequestFilterSchema(Schema):
    """
    For numeric comparison in the clause.
    """
    target = fields.String(required=True, description='The field to compare.', example='name')
    expr = fields.String(required=True, description='The expression to compare to the field.', example='apache')


class QueryRequestClauseSchema(Schema):
    """
    Represents a clause to filter a item based on various conditions.
    """
    _and = fields.Nested('self', data_key='and', many=True,
                         description='All the clause has to be satisfied.', example="""
                            [
                                {
                                    "equal": {
                                        "target": "name",
                                        "expr:": "apache"
                                        }
                                    },
                                    {
                                    "lte": {
                                        "target": "timeout",
                                        "expr": 5
                                    }
                            ]""")
    _or = fields.Nested('self', data_key='or', many=True,
                       description='At least the clause has to be satisfied.', example="""
                            [
                                {
                                    "equal": {
                                        "target": "name",
                                        "expr:": "apache"
                                        }
                                    },
                                    {
                                    "lte": {
                                        "target": "timeout",
                                        "expr": 5
                                    }
                            ]""")
    _not = fields.Nested('self', data_key='not',
                       description='The clause has to be not satisfied.')
    lte = fields.Nested(QueryRequestFilterSchema, description='The target field must be lower or equal to the expr value.')
    gte = fields.Nested(QueryRequestFilterSchema, description='The target field must be greater or equal to the expr value.')
    lt = fields.Nested(QueryRequestFilterSchema, description='The target field must be lower than the expr value.')
    gt = fields.Nested(QueryRequestFilterSchema, description='The target field must be greater to the expr value.')
    equal = fields.Nested(QueryRequestFilterSchema, description='The target field must be equal to the expr value.')
    reg_exp = fields.Nested(QueryRequestFilterSchema,
                            description='The target field must be satisfy the regular expression in expr.')


class QueryRequestOrderSchema(Schema):
    """
    Order the filtered items.
    """
    target = fields.String(required=True, description='The field to compare.', example='name')
    mode = fields.String(enum=['asc', 'desc'], required=True, description='Order mode.', example='asc')


class QueryRequestLimitSchema(Schema):
    """
    Limit the items to return.
    """
    _from = fields.Integer(data_key='from', description='Started index of the items to return.', example=1)
    _to = fields.Integer(data_key='to', description='Ended index of the items to return.', example=5)


class QueryRequestSchema(Schema):
    """
    Query request to filter the items.
    """
    select = fields.List(fields.String(), description='Fields to return.', example='[id, name]')
    where = fields.Nested(QueryRequestClauseSchema, description='Filter the items based on different conditions.')
    order = fields.Nested(QueryRequestOrderSchema, many=True, description='Order the filtered items.')
    limit = fields.Nested(QueryRequestLimitSchema, description='Limit the number of items to return.')
