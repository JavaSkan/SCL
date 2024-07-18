from runtime import errors as err

_ALCS     = dict()    #Allocations
_ALSS     = dict()    #Aliases
_FUN_RET  = None      #Function return
_ERR_CODE = 0         #Error Code

def exists(identifier: str) -> bool:
    for v in _ALCS:
        if v.ident == identifier:
            return True
    return False

@err.dangerous()
def alloc(element):
    if (existing_e := _ALCS.get(element.ident)) == None:
        element.maddr = len(_ALCS) - 1
        _ALCS[element.ident] = element
    else:
        return err.SCLAlreadyExistingError(element.ident,existing_e)

@err.dangerous()
def de_alloc(element):
    try:
        _ALCS.pop(element.ident)
    except KeyError:
        return err.SCLNotFoundError(element.ident)


@err.dangerous()
def get_from_id(identifier: str):
    e = _ALCS.get(identifier)
    return e or err.SCLNotFoundError(identifier)

def get_value_from_id(id):
    var = get_from_id(id)
    return var.get_value()