from marshmallow import fields, Schema


class RecipeActionSchema(Schema):
    """
    Action part in a single item of the recipe.
    """
    cmd = fields.String(required=True,
                        description='Command.')
    args = fields.List(fields.String(description='Single command argument.', example='-al'),
                       description='Command arguments.')


class RecipeParameterSchema(Schema):
    """
    Parameter part in a single item of the recipe.
    """
    destination = fields.String(required=True, description='Destination filename.', example='filebeat.yml')
    name = fields.String(required=True, description='Parameter name.', example='period')
    sep = fields.String(required=True, description='Separator between name and value.', example='=')
    value = fields.String(required=True, description='Parameter new value.', example='10s')


class RecipeResourceSchema(Schema):
    """
    Resource part in a single item of the recipe.
    """
    destination = fields.String(required=True, description='Destination filename', example='filebeat.yml')
    content = fields.String(required=True, description='Resource content.')


class RecipeSchema(Schema):
    """
    Recipe Schema.
    """
    actions = fields.Nested(RecipeActionSchema, many=True, description='Actions.')
    parameters = fields.Nested(RecipeParameterSchema, many=True, description='Parameters.')
    resources = fields.Nested(RecipeResourceSchema, many=True, description='Resources.')
