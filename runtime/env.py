from runtime import allocable as al, errors as err

_VARS = []            #variables
_FUN_RET = None       #Function return
_ERR_CODE = 0         #Error Code
_VARREF_SYM = '$'     #Variable reference symbol

def get_from_id(id_: str):
    for v in _VARS:
        if v.ident == id_:
            return v
    return None

def get_value_from_id(id):
    var = get_from_id(id)
    if type(var) is al.Variable:
        return var.get_value()
    else:
        try:
            return var.vl
        except AttributeError:
            err.SCLNotFoundError(id).trigger()