import tuierrors
import env
import funlink as fl
import tuiparsing


def is_var_ref(id:str) -> bool:
    return id.startswith(env._VARREF_SYM) and len(id) > 1

#TODO consider updating var_ref(), make it return the actual value, not as a string, and replacing function calls by 'str(var_ref(...))'
def var_ref(id: str) -> str:
    return str(env.get_value_from_id(id[1:]))

def is_valid_name(name: str) -> bool:
    return name.isidentifier()

def execute(inst):
    parsed = tuiparsing.parse(inst)
    if (command_fun:=fl.cmds.get((command_id := parsed[0].value))):
        err = command_fun(parsed[1:])
        if err:
            err.trigger(line=inst)
    else:
        tuierrors.TuiUnknownCommand(command_id).trigger(line=inst)

def execute_block(block: list):
    for ins in block:
        if type(ins) is str:
            execute(ins)
        elif type(ins) is list:
            execute_block(ins)