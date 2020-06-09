from marshmallow import Schema, validates_schema, ValidationError
from schema.validate import msg_id_already_found, msg_id_multiple_times, msg_id_not_found, \
                            msg_present_in_request_uri, msg_readonly


class BaseSchema(Schema):
    ids = []

    @validates_schema
    def validate_id(self, data, **kwargs):
        id = data.get('id', None)
        ids = self.doc_cls.get_ids()
        if self.method == 'POST' and id in ids:
            raise ValidationError(dict(id=[msg_id_already_found]))
        elif self.method in ['PUT', 'DELETE'] and id not in ids:
            raise ValidationError(dict(id=[msg_id_not_found]))

    @validates_schema
    def validate_readonly(self, data, **kwargs):
        if self.method == 'PUT':
            for field, props in self.declared_fields.items():
                if props.metadata.get('readonly', False) and data.get(field, None) is not None:
                        raise ValidationError({field: msg_readonly})


class NestedSchema(Schema):
    pass
