from http import HTTPStatus
from marshmallow import fields, Schema


class ResponseSchema(Schema):
    """
    Response for the item creation.
    """
    status = fields.String(required=True, enum=['created', 'noop', 'updated', 'deleted'],
                           description='Status of the operation.', example='created')
    data = fields.Dict(required=True, description='Data of the item.',
                       keys=fields.String(required=True, description='Field name.',
                                          example='id'),
                       values=fields.Raw(required=True, description='Field value.',
                                         example='vCPPaXABjPI5oepgPuyz'))
    http_status_code = fields.Integer(required=True, enum=[HTTPStatus.CREATED, HTTPStatus.OK],
                                      description='HTTP Status Code', example=HTTPStatus.CREATED)


class ErrorSchema(Schema):
    """
    Response in case of error.
    """
    status = fields.String(required=True, enum=['error'],
                           description='Indicate an error', example='error')
    reason = fields.String(required=True,
                           description='Human readable message that describes the error.',
                           example='Request not valid: two ids provided')
    id = fields.String(required=True,  description='id of the item.',
                       example='x4fgctkm4MXQOUHYjIag')
    http_status_code = fields.Integer(required=True, enum=[HTTPStatus.CONFLICT],
                                      description='HTTP Status code', example=HTTPStatus.CONFLICT)


class HTTPErrorSchema(Schema):
    """
    HTTP Error Schema.
    """
    title = fields.String(required=True, description='Title error',
                          example='400 Bad Request')
    description = fields.String(required=True, description='Human readable message that describes the error.',
                                example='Could not decode the request body, either because it was not valid JSON or because it was not encoded as UTF-8.')
