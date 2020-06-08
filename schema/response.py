from http import HTTPStatus
from marshmallow import Schema, validate
from marshmallow.fields import Bool, Dict, Integer, Raw, Str


response_status = ['created', 'noop', 'updated', 'deleted', 'error']
response_http_status_codes = [HTTPStatus.CONFLICT, HTTPStatus.CREATED, HTTPStatus.NOT_FOUND,
                              HTTPStatus.OK, HTTPStatus.UNPROCESSABLE_ENTITY]


class ResponseSchema(Schema):
    """Response for the item creation."""

    status = Str(required=True, enum=response_status, example=response_status[0],
                 description='Status of the operation.',
                 validate=validate.OneOf(response_status))

    error = Bool(default=False, example=False,
                 description='Indicate the presence of an error')

    description = Str(required=True, example='Request not valid: two ids provided.',
                      description='Human readable message that describes the status of the operation.')

    exception = Str(example='Value required.',
                    description='Message of the occurred exception.')

    data = Dict(keys=Str(required=True, example='id', description='Field name.'),
                values=Raw(required=True, example='apache',
                           description='Field value.'),
                required=True,
                description='Data of the item.')

    http_status_code = Integer(required=True, enum=response_http_status_codes, example=response_http_status_codes[0],
                               description='HTTP Status Code.',
                               validate=validate.OneOf(response_http_status_codes))


class HTTPErrorSchema(Schema):
    """HTTP Error Schema."""

    title = Str(required=True, example='400 Bad Request',
                description='Title error')

    description = Str(required=True, example="""Could not decode the request body, either because it was not
                                                valid or because it was not encoded as UTF-8.""",
                      description='Human readable message that describes the error.')
