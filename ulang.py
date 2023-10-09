import TuiErrors
import env
import funlink as fl
import tuiparsing


def gethead(args: list):
    try:
        return args[0]
    except IndexError:
        return ""

def is_var_ref(id:str) -> bool:
    return id.startswith(env._VARREF_SYM) and len(id) > 1

#TODO consider updating var_ref(), make it return the actual value, not as a string, and replacing function calls by 'str(var_ref(...))'
def var_ref(id: str) -> str:
    if is_var_ref(id):
        return str(env.get_value_from_id(id[1:]))
    return id

def is_valid_name(name: str) -> bool:
    return name.isidentifier()

def execute(inst):
    try:
        parsed = tuiparsing.parse_tokens(inst)
        fl.cmds[gethead(parsed)](parsed[1:])
    except KeyError:
        TuiErrors.TuiError('Unknown Command').trigger()
    except IndexError:
        TuiErrors.TuiError('Args don\'t match').trigger()

def execute_block(block: list):
    for ins in block:
        if type(ins) is str:
            execute(ins)
        elif type(ins) is list:
            execute_block(ins)