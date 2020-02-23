from http import HTTPStatus
from marshmallow import fields, Schema


class IdNotFoundSchema(Schema):
    """
    id not present in the request.
    """
    status = fields.String(required=True, enum=['error'], description='Indicate an error.',
                           example='error')
    reason = fields.String(required=True, enum=['id property not found'],
                           description='Human readable message that describes the error.', example='id property not found')


class TwoIdsProvidedSchema(Schema):
    """
    id provided two times.
    """
    status = fields.String(required=True, enum=['error'],
                           description='Indicate an error', example='error')
    id = fields.List(fields.String(required=True, description='Provided id.',
                                   example='x4fgctkm4MXQOUHYjIag'), required=True)
    reason = fields.String(required=True, enum=['Request not valid: two ids provided'],
                           description='Human readable message that describes the error.',
                           example='Request not valid: two ids provided')
    http_status_code = fields.Integer(required=True, enum=[HTTPStatus.CONFLICT],
                                      description='HTTP Status Code', example=HTTPStatus.CONFLICT)
