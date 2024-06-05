from parser.tokens import Token
from . import errors
from parser.tokenizing import Lexer
from parser.parsing import Parser

SCL_LEXER  = Lexer("")
SCL_PARSER = Parser([])

def execute(inst: str | list[Token]) -> None:
    global SCL_LEXER, SCL_PARSER

    errors.CURRENT_LINE = inst if type(inst) is str else errors.CURRENT_LINE
    from commands.funlink import cmds

    if type(inst) is str:
        SCL_LEXER.reset(inst)
        SCL_PARSER.reset(SCL_LEXER.tokenize())
    else:
        SCL_PARSER.reset(new=inst)
    parsed = SCL_PARSER.parse()
    if len(parsed) != 0:
        if (command_fun:= cmds.get((command_id := parsed[0].value))):
            err = command_fun(parsed[1:])
            if err:
                err.trigger(line=errors.CURRENT_LINE)
        else:
            errors.SCLUnknownCommandError(command_id).trigger(line=errors.CURRENT_LINE)