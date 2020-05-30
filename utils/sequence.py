def subset(elements, *keys, negation=False):
    def match(element):
        if negation:
            return element[0] not in keys
        else:
            return element[0] in keys
    return dict(filter(match, elements.items()))


def wrap(data):
    """
    Wrap the data if an array if it is ont a list of tuple.

    :param data: data to wrap
    :returns: wrapped data
    """
    return data if type(data) in [list, tuple] else [data]
