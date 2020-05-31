from marshmallow import Schema
from marshmallow.fields import String


class QueryRequestOrderSchema(Schema):
    """
    Order the filtered items.
    """

    target = String(required=True, description='The field to compare.', example='name')

    mode = String(required=True, enum=['asc', 'desc'], description='Order mode.',
                  example='desc', default='asc')
