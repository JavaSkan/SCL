_VARS = []
_BOOL = False

def get_value_from_id(id):
    for v in _VARS:
        if v.id == id:
            return v.repr_val()
    print(f"WARNING: '{id}' is not defined")

def get_from_id(id):
    for v in _VARS:
        if v.id == id:
            return v
    print(f"WARNING: '{id}' is not defined")