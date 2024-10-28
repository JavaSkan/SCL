from runtime import errors as err

class Environment:

    def __init__(self):
        self.allocations = {}
        self.aliases = {}
        self.fun_ret = None
        self.exit_code = 0
        self.prev_env = None

    def alloc(self,element):
        if (existing_e := self.allocations.get(element.ident)) == None:
            self.allocations[element.ident] = element
        else:
            return err.SCLAlreadyExistingError(element.ident, existing_e)

    def de_alloc(self,element):
        try:
            self.allocations.pop(element.ident)
        except KeyError:
            return err.SCLNotFoundError(element.ident)

    def get_from_id(self,identifier: str):
        e = self.allocations.get(identifier)
        return e or err.SCLNotFoundError(identifier)

    def get_value_from_id(self,identifier: str):
        var = get_from_id(identifier)
        return var.get_value()

    def use_this_env(self):
        global CURENV
        self.prev_env = CURENV
        CURENV = self

    def quit(self,exit_code = 0):
        self.allocations.clear()
        self.aliases.clear()
        self.exit_code = exit_code

CURENV = Environment() # Current Environment

@err.dangerous()
def alloc(element):
    # if (existing_e := _ALCS.get(element.ident)) == None:
    #     element.maddr = len(_ALCS) - 1
    #     _ALCS[element.ident] = element
    # else:
    #     return err.SCLAlreadyExistingError(element.ident,existing_e)
    return CURENV.alloc(element)

@err.dangerous()
def de_alloc(element):
    # try:
    #     _ALCS.pop(element.ident)
    # except KeyError:
    #     return err.SCLNotFoundError(element.ident)
    return CURENV.de_alloc(element)


@err.dangerous()
def get_from_id(identifier: str):
    # e = _ALCS.get(identifier)
    # return e or err.SCLNotFoundError(identifier)
    return CURENV.get_from_id(identifier)

def get_value_from_id(id):
    var = get_from_id(id)
    return var.get_value()