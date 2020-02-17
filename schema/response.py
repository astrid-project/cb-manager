from marshmallow import fields, Schema


class CreateResponseSchema(Schema):
    """
    Response for the item creation.
    """
    id = fields.String(description='id of the created item.', example='apache')
    status = fields.String(description='Status of the operation.', example='created')


class UpdateResponseSchema(Schema):
    """
    Response for the item update.
    """
    id = fields.String(description='id of the updated item.', example='apache')
    status = fields.String(enum=['noop', 'updated'], description='Status of the operation.', example='noop')


class ReadResponseSchema(Schema):
    """
    Response for the item read.
    """
    id = fields.String(description='id of the updated item.', example='apache')
    status = fields.String(enum=['noop', 'updated'], description='Status of the operation.', example='noop')


class DeleteResponseSchema(Schema):
    """
    Response for the item deletetion.
    """
    id = fields.String(description='id of the updated item.', example='apache')
    status = fields.String(enum=['noop', 'updated'], description='Status of the operation.', example='noop')
