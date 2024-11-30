from parser.tokens import Token
from . import errors
from . import env
from parser.tokenizing import Lexer
from parser.parsing import Parser

SCL_LEXER  = Lexer()
SCL_PARSER = Parser()

def execute(inst: str | list[Token]) -> None:
    global SCL_LEXER, SCL_PARSER

    errors.CURRENT_LINE = inst if type(inst) is str else errors.CURRENT_LINE
    from commands.funlink import cmds

    if type(inst) is str:
        #check if the inst is an alias
        al_or_inst = env.CURENV.aliases.get(inst) or inst
        SCL_LEXER.reset(al_or_inst)
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

class Executor:

    def __init__(self,environment=env.CURENV):
        #TODO find out why enviroment param is not eq to env.CURENV when doing with Executor(): ...
        self.line   = ''
        self.lexer  = Lexer()
        self.parser = Parser()
        self.evm    = environment

    def __enter__(self):
        self.init()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.reset_env()

    def load_script(self, script: str):
        self.line = script
        self.lexer.reset(self.line)
        self.parser.reset(self.lexer.tokenize())

    def init(self):
        if self.evm != env.CURENV:
            self.evm.use_this_env()

    def reset_env(self):
        if self.evm.prev_env != None:
            env.CURENV = self.evm.prev_env

    def execute(self, script: str | list):
        if type(script) is str:
            self.load_script(self.evm.aliases.get(script) or script)
            errors.CURRENT_LINE = self.line
        else:
            self.parser.reset(new=script)
        parsed = self.parser.parse()
        self.execute_parsed(parsed)

    def execute_parsed(self, parsed: list[Token]):
        from commands.funlink import cmds
        if len(parsed) != 0:
            if (command_fun := cmds.get((command_id := parsed[0].value))):
                err = command_fun(parsed[1:])
                if err:
                    err.trigger(line=self.line)
            else:
                errors.SCLUnknownCommandError(command_id).trigger(line=self.line)