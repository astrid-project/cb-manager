from marshmallow import fields, Schema


class IdNotFoundSchema(Schema):
    """
    id not present in the request.
    """
    status = fields.String(required=True, enum=['error'], description='Indicate an error.', example='error')
    title = fields.String(required=True, enum=['Request not valid'], description='Title error', example='Request not valid')
    description = fields.String(required=True, enum=['id property not found'],
                                description='Human readable message that describes the error.', example='id property not found')


class IdProvidedSchema(Schema):
    """
    id provided multiple times.
    """
    id = fields.String(required=True, description='id of the item found.', example='apache')
    status = fields.String(required=True, enum=['error'], description='Indicate an error', example='error')
    title = fields.String(required=True, descripion='Title error.', example='Agent Catalog already found')
    description = fields.String(required=True, enum=['id already present'],
                                description='Human readable message that describes the error.', example='id already present')
