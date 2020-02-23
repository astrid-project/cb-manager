from http import HTTPStatus
from marshmallow import fields, Schema


class ItemFoundSchema(Schema):
    """
    Conflict error during creation: item with the same id already present.
    """
    status = fields.String(required=True, enum=['error'],
                           description='Indicate an error', example='error')
    reason = fields.String(required=True, enum=['id already present'],
                           description='Human readable message that describes the error.',
                           example='id already present')
    id = fields.String(required=True,  description='id of the item to create.',
                       example='x4fgctkm4MXQOUHYjIag')
    http_status_code = fields.Integer(data_key='http-status-code', required=True,
                                      enum=[HTTPStatus.CONFLICT],
                                      description='HTTP Status code', example=HTTPStatus.CONFLICT)


class ItemNotFoundSchema(Schema):
    """
    Item not present.
    """
    status = fields.String(required=True, enum=['error'],
                           description='Indicate an error', example='error')
    reason = fields.String(required=True, enum=['id already present'],
                           description='Human readable message that describes the error.', example='id not found')
    id = fields.String(required=True, description='id of the item.',
                       example='apx4fgctkm4MXQOUHYjIagache')
    http_status_code = fields.Integer(data_key='http-status-code', required=True,
                                      enum=[HTTPStatus.NOT_FOUND],
                                      description='HTTP Status code', example=HTTPStatus.NOT_FOUND)
