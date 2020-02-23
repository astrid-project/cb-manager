from marshmallow import fields, Schema


class NotFoundSchema(Schema):
    """
    Resource not found.
    """
    title = fields.String(required=True, description='Title error',
                          example='404 Not found')
    description = fields.String(required=True, description='Human readable message that describes the error.',
                                example='The resource is not found.')
