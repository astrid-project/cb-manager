from http import HTTPStatus
from marshmallow import fields, Schema


class CreateResponseSchema(Schema):
    """
    Response for the item creation.
    """
    status = fields.String(required=True,
                           enum=['created'],
                           description='Status of the operation.',
                           example='created')
    data = fields.Dict(required=True,
                       description='Data of the created item.',
                       keys=fields.String(required=True,
                                          description='Field name.',
                                          example='id'),
                       values=fields.Raw(required=True,
                                         description='Field value.',
                                         example='vCPPaXABjPI5oepgPuyz'))
    http_status_code = fields.Integer(data_key='http-status-code',
                                      enum=[HTTPStatus.CREATED],
                                      description='HTTP Status Code',
                                      example=HTTPStatus.CREATED)


class UpdateResponseSchema(Schema):
    """
    Response for the item update.
    """
    status = fields.String(required=True,
                           enum=['noop', 'updated'],
                           description='Status of the operation.',
                           example='noop')
    data = fields.Dict(required=True, description='Data of the updated item.',
                       keys=fields.String(required=True,
                                          description='Field name.',
                                          example='id'),
                       values=fields.Raw(required=True,
                                         description='Field value.',
                                         example='vCPPaXABjPI5oepgPuyz'))
    http_status_code = fields.Integer(data_key='http-status-code',
                                      enum=[HTTPStatus.CREATED],
                                      description='HTTP Status Code',
                                      example=HTTPStatus.OK)


class DeleteResponseSchema(Schema):
    """
    Response for the item deletetion.
    """
    status = fields.String(required=True,
                           enum=['deleted'],
                           description='Status of the operation.',
                           example='deleted')
    data = fields.Dict(required=True,
                       description='Data of the delted item.',
                       keys=fields.String(required=True,
                                          description='Field name.',
                                          example='id'),
                       values=fields.Raw(required=True,
                                         description='Field value.',
                                         example='vCPPaXABjPI5oepgPuyz'))
    http_status_code = fields.Integer(data_key='http-status-code',
                                      enum=[HTTPStatus.CREATED],
                                      description='HTTP Status Code',
                                      example=HTTPStatus.OK)
