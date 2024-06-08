from runtime import allocable as al, errors as err

_VARS = []            #variables
_FUN_RET = None       #Function return
_ERR_CODE = 0         #Error Code

def exists(identifier: str) -> bool:
    for v in _VARS:
        if v.ident == identifier:
            return True
    return False

@err.dangerous()
def alloc(element):
    if not (element.ident in [(existing_e := e).ident for e in _VARS]):
        element.maddr = len(_VARS)-1
        _VARS.append(element)
    else:
        return err.SCLAlreadyExistingError(element.ident,existing_e)

@err.dangerous()
def de_alloc(element):
    try:
        _VARS.remove(element)
    except ValueError:
        return err.SCLNotFoundError(element.ident)


@err.dangerous()
def get_from_id(identifier: str):
    for v in _VARS:
        if v.ident == identifier:
            return v
    return err.SCLNotFoundError(identifier)

def get_value_from_id(id):
    var = get_from_id(id)
    return var.get_value()