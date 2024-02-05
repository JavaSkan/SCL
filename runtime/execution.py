from parser import parsing
from . import errors

def execute(inst):
    import commands.funlink
    parsed = parsing.parse(inst)
    if (command_fun:= commands.funlink.cmds.get((command_id := parsed[0].value))):
        err = command_fun(parsed[1:])
        if err:
            err.trigger(line=inst)
    else:
        errors.SCLUnknownCommandError(command_id).trigger(line=inst)

def execute_block(block: list):
    for ins in block:
        if type(ins) is str:
            execute(ins)
        elif type(ins) is list:
            execute_block(ins)