from datetime import datetime

class Validate:
    @staticmethod
    def is_hostname(x):
        return isinstance(x, str)

    @staticmethod
    def is_name(x):
        return isinstance(x, str)

    @staticmethod
    def is_boolean(x):
        return isinstance(x, bool)

    @staticmethod
    def is_datetime(x):
        return isinstance (x, datetime)

    @staticmethod
    def is_id(x):
        return isinstance(x, str) and \
                x.islower() and \
                    x.isprintable() and \
                        not x.isspace()

    @staticmethod
    def is_str(x):
        return isinstance(x, str)

    @staticmethod
    def is_list(x):
        return isinstance(x, list)

    @staticmethod
    def is_single_choice(*vals):
        return lambda x: not Validate.is_list(x) and \
                        x in vals

    @staticmethod
    def is_multiple_choice(*vals):
        return lambda x: Validate.is_single_choice(vals) or \
                            all(item in vals for item in x)

    @staticmethod
    def is_obj(obj):
        return lambda x: obj.error.validate_properties(**x, include_required = True)

    @staticmethod
    def is_list_unique_type(cls):
        return lambda x: Validate.is_list(x) and \
                            all(isinstance(item, cls) for item in x)

    @staticmethod
    def is_list_unique_value(x):
        return Validate.is_list(x) and len(set(x)) == len(x)

    @staticmethod
    def is_list_obj(obj, unique_by = None):
        return lambda x: isinstance(x, list) and \
                            all(obj.error.validate_properties(**item, include_required = True) for item in x) and \
                                (not unique_by or Validate.is_list_unique_value([item[unique_by] for item in x]))
