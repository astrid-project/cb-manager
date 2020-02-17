from marshmallow import fields, Schema


class ItemFoundSchema(Schema):
    """
    Conflict error during creation: item with the same id already present.
    """
    id = fields.String(required=True, description='id of the item to create.', example='apache')
    status = fields.String(required=True, enum=['error'], description='Indicate an error', example='error')
    title = fields.String(required=True, descripion='Title error.', example='Agent Catalog already found')
    description = fields.String(required=True, enum=['id already present'],
                                description='Human readable message that describes the error.', example='id already present')


class ItemNotFoundSchema(Schema):
    """
    Item not present.
    """
    id = fields.String(required=True, description='id of the item.', example='apache')
    status = fields.String(required=True, enum=['error'], description='Indicate an error', example='error')
    title = fields.String(required=True, enum=['Request not valid'], descripion='Title error.', example='Request not valid')
    description = fields.String(required=True, enum=['id already present'],
                                description='Human readable message that describes the error.', example='id not found')
