import utils


class Args:
    """
    Simple class to store the program arguments.
    """

    db = None

    @classmethod
    def set(cls, args, convert_to_seconds=()):
        """
        Set the arguments and convert the fields in seconds from the human format (e.g.: 1min)

        :params cls: Args class
        :params args: arguments
        :convert_to_seconds: fields to convert in seconds from the human format (e.g.: 1min)
        """
        cls.db = args
        cls.convert_to_seconds(*convert_to_seconds)

    @classmethod
    def convert_to_seconds(cls, *fields):
        """
        Convert to seconds all fields where the is in human format (e.g.: 1min)

        :params cls: Args class
        :params fields: all the fields to convert
        """
        for field in fields:
            setattr(cls.db, field, utils.get_seconds(getattr(cls.db, field)))
