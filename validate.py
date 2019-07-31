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
        return isinstance(x, str) and x.islower() and x.isprintable() and not x.isspace()