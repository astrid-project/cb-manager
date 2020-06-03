from http import HTTPStatus
from marshmallow import Schema
from marshmallow.fields import Bool, Dict, Integer, Raw, Str


class ResponseSchema(Schema):
    """Response for the item creation."""
    status = Str(required=True, enum=['created', 'noop', 'updated', 'deleted', 'error'],
                 description='Status of the operation.', example='created')
    error = Bool(default=False, example=False,
                 description='Indicate the presence of an error')
    description = Str(required=True, example='Request not valid: two ids provided.',
                      description='Human readable message that describes the status of the operation.')
    exception = Str(description='Message of the occurred exception.', example='Value required.')
    data = Dict(required=True, description='Data of the item.',
                keys=Str(required=True, description='Field name.', example='id'),
                values=Raw(required=True, description='Field value.', example='apache'))
    http_status_code = Integer(required=True, description='HTTP Status Code', example=HTTPStatus.CREATED,
                               enum=[HTTPStatus.CONFLICT, HTTPStatus.CREATED,
                                     HTTPStatus.NOT_FOUND, HTTPStatus.OK, HTTPStatus.UNPROCESSABLE_ENTITY])


class HTTPErrorSchema(Schema):
    """HTTP Error Schema."""
    title = Str(required=True, description='Title error',
                example='400 Bad Request')
    description = Str(required=True, description='Human readable message that describes the error.',
                      example="""Could not decode the request body, either because it was not
                                 valid JSON or because it was not encoded as UTF-8.""")
