import allocable as al
import ulang
_VARS = []
_BOOL = False
_FUN_RET = None

def get_from_id(id):
    for v in _VARS:
        if v.id == id:
            return v
    return None

def get_value_from_id(id):
    var = get_from_id(id)
    match var:
        case al.Variable:
            return var.get_value
        case _:
            try:
                return var.vl
            except AttributeError:
                print(f"There is no field with id '{id}'")
                quit()