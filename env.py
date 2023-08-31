import allocable as al
import TuiErrors as terr

_VARS = []        #variables
_BOOL = False     #boolean result
_FUN_RET = None   #Function return
_VARREF_SYM = '$' #Variable reference symbol

def get_from_id(id: str):
    for v in _VARS:
        if v.id == id:
            return v
    return None

def get_value_from_id(id):
    var = get_from_id(id)
    if (vtype := type(var)) is al.Variable:
        return var.get_value()
    else:
        try:
            return var.vl
        except AttributeError:
            raise terr.TuiNotFoundError(id)