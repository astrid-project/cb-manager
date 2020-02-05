def wrap(data):
    return data if type(data) is list else [data]

def fix_target(prop):
    return '_id' if prop == 'id' else prop
