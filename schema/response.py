from http import HTTPStatus
from marshmallow import Schema
from marshmallow.fields import Boolean, Dict, Integer, Raw, String


class ResponseSchema(Schema):
    """
    Response for the item creation.
    """

    status = String(required=True, enum=['created', 'noop', 'updated', 'deleted', 'error'],
                    description='Status of the operation.', example='created')

    error = Boolean(default=False, description='Indicate the presence of an error', example=False)

    description = String(required=True,
                         description='Human readable message that describes the status of the operation.',
                         example='Request not valid: two ids provided.')

    data = Dict(required=True, description='Data of the item.',
                keys=String(required=True, description='Field name.', example='id'),
                values=Raw(required=True, description='Field value.', example='apache'))

    http_status_code = Integer(required=True,
                               enum=[HTTPStatus.CONFLICT, HTTPStatus.CREATED,
                                     HTTPStatus.NOT_FOUND, HTTPStatus.OK, HTTPStatus.UNPROCESSABLE_ENTITY],
                               description='HTTP Status Code', example=HTTPStatus.CREATED)
