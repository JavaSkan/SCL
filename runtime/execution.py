from parser import parsing
from . import errors

def execute(inst):
    errors.CURRENT_LINE = inst
    from commands.funlink import cmds
    parsed = parsing.parse(inst)
    if (command_fun:= cmds.get((command_id := parsed[0].value))):
        err = command_fun(parsed[1:])
        if err:
            err.trigger(line=inst)
    else:
        errors.SCLUnknownCommandError(command_id).trigger(line=inst)