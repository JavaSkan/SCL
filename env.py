_VARS = []
_BOOL = False

def get_from_id(id):
    for v in _VARS:
        if v.id == id:
            return v
    return None

def get_value_from_id(id):
    return get_from_id(id)