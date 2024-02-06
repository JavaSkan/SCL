from runtime import allocable as al, errors as err

_VARS = []            #variables
_FUN_RET = None       #Function return
_ERR_CODE = 0         #Error Code
_VARREF_SYM = '$'     #Variable reference symbol

def alloc(element):
    if not (existing := get_from_id(element.ident)):
        element.maddr = len(_VARS)-1
        _VARS.append(element)
    else:
        err.SCLAlreadyExistingError(existing.ident,existing).trigger()

def de_alloc(element):
    _VARS.pop(element.maddr)

def get_from_id(id_: str):
    for v in _VARS:
        if v.ident == id_:
            return v
    return None

def get_value_from_id(id):
    var = get_from_id(id)
    if not var:
        err.SCLNotFoundError(id).trigger()
    if type(var) is al.Variable:
        return var.get_value()
    else:
        return var.vl