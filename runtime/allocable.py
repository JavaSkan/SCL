from enum import Enum, auto

import parser.parsing
from runtime import errors as err, env as ev
from runtime.env import Environment
from runtime.execution import Executor
from parser.parsing import TokenType, Token

class DT_TYPES(Enum):

    INT  = auto()
    FLT  = auto()
    STR  = auto()
    BOOL = auto()
    ANY  = auto()
    NIL  = auto()

    def __repr__(self):
        return self.name

    def to_python_type(self):
        match self:
            case DT_TYPES.INT:
                return int
            case DT_TYPES.FLT:
                return float
            case DT_TYPES.STR:
                return str
            case DT_TYPES.BOOL:
                return bool
            case DT_TYPES.ANY:
                return object
            case DT_TYPES.NIL:
                return None

    def str_to_type(str_type: str):
        match str_type:
            case 'int':
                return DT_TYPES.INT
            case 'flt':
                return DT_TYPES.FLT
            case 'str':
                return DT_TYPES.STR
            case 'bool':
                return DT_TYPES.BOOL
            case 'nil':
                return DT_TYPES.NIL
            # 'any' or everything else
            case _:
                return DT_TYPES.ANY

    def guess_type(str_value: str):
        if str_value.isdigit() or str_value.startswith('-') and str_value[1:].isdigit():
            return DT_TYPES.INT
        elif (p := str_value.replace('.', '', 1)).isdigit() or p.startswith('-') and p[1:].isdigit():
            return DT_TYPES.FLT
        elif str_value == 'true' or str_value == 'false':
            return DT_TYPES.BOOL
        elif str_value == 'nil':
            return DT_TYPES.NIL
        else:
            return DT_TYPES.STR

    def default_value(self):
        match self:
            case DT_TYPES.INT:
                return 0
            case DT_TYPES.FLT:
                return 0.0
            case DT_TYPES.BOOL:
                return True
            case DT_TYPES.STR:
                return ''
            case DT_TYPES.NIL:
                return None

    def get_literal_version(self):
        match self:
            case DT_TYPES.INT:
                return TokenType.INT
            case DT_TYPES.FLT:
                return TokenType.FLT
            case DT_TYPES.STR:
                return TokenType.STR
            case DT_TYPES.BOOL:
                return TokenType.BOOL
            #No literal type for nil type

    def convert_str_to_value(self,str_value):
        str_value = str_value.lower() # for ex: True -> true
        match self:
            case DT_TYPES.INT:
                return int(str_value)
            case DT_TYPES.FLT:
                return float(str_value)
            case DT_TYPES.STR:
                return str_value
            case DT_TYPES.BOOL:
                return str_value == 'true' or not (str_value == 'false')
            case DT_TYPES.NIL:
                return None

    def is_compatible_with_type(self,str_value):
        match self:
            case DT_TYPES.INT:
                return str_value.isdigit() or str_value.startswith('-') and str_value[1:].isdigit()
            case DT_TYPES.FLT:
                return (p := str_value.replace('.', '', 1)).isdigit() or p.startswith('-') and p[1:].isdigit()
            case DT_TYPES.STR:
                return True
            case DT_TYPES.BOOL:
                str_value = str_value.lower() #ex: True => true
                return str_value == 'true' or str_value == 'false'
            case DT_TYPES.NIL:
                return str_value == 'nil'

class VARKIND(Enum):
    MUT = auto()
    CONST = auto()
    TEMP = auto()

    def str_to_varkind(str_kind: str):
        match str_kind:
            case "mut":
                return VARKIND.MUT
            case "const":
                return VARKIND.CONST
            case "temp":
                return VARKIND.TEMP
    def __repr__(self):
        match self.name:
            case VARKIND.MUT.name:
                return "mut"
            case VARKIND.CONST.name:
                return "cst"
            case VARKIND.TEMP.name:
                return "tmp"
            case _:
                return "unknown varkind"

class Iterable:
    def __init__(self,items):
        self.items = items
        self.length = len(self.items)

    @err.dangerous("[RUNTIME] GET VALUE FROM ITERABLE")
    def get_at_index(self, index: int):
        if 0 <= index < self.length:
            return self.items[index]
        return err.SCLIndexOutOfBoundError(index, self.length)

    @err.dangerous("[RUNTIME] SET VALUE IN ITERABLE")
    def set_at_index(self,index: int, value):
        if 0 <= index < self.length:
            self.items[index] = value
        else:
            return err.SCLIndexOutOfBoundError(index, self.length)

    def get_items_gen(self):
        for e in self.items:
            yield e

class Allocable:

    def __init__(self, type: DT_TYPES, ident:str, value):
        self.maddr = id(self)
        self.type = type
        self.ident = ident
        self.vl = value

    def __repr__(self):
        return f"[{self.type} {self.ident}: {self.vl}]"

    def get_value(self):
        return self.vl

    # To inject in python code (eg: string value abc to "abc")
    def get_insertion_value(self):
        if self.type == DT_TYPES.STR:
            return f'"{self.get_value()}"'
        else:
            return str(self.get_value())

    def set_value(self,new):
        self.vl = new

class Variable(Allocable):

    #TODO implement variable kind temp
    def __init__(self, kind:VARKIND, type:DT_TYPES,ident:str, value):
        self.kind = kind
        super().__init__(type, ident, value)

    def get_value(self):
        return super().get_value()

    def set_value(self,new):
        if self.kind == VARKIND.CONST:
            err.SCLModifyConstantError(self.ident).trigger()
        super().set_value(new)


    def __repr__(self):
        return f"Var {self.ident}<{self.kind.name} {self.type.name}>({self.vl})"

class Array(Allocable,Iterable):

    def __init__(self, type: DT_TYPES, ident:str, vars: list):
        super().__init__(type, ident, vars)
        Iterable.__init__(self,vars)

    def __repr__(self):
        out = f"Array {self.ident}<{self.type.name}>:["
        for (i,e) in enumerate(self.items):
            out += f"{e}{',' if i < self.length-1 else ''}"
        out += "]"
        return out

    def are_values_compatible_with_type(self,values):
        for v in values:
            if type(v) is not self.type.to_python_type():
                return False
        return True


class Function(Allocable):

    def __init__(self, type:DT_TYPES, ident:str, params, body:list[str]):
        self.pm = params or []
        self.bd = body
        self.locals = []
        self.ret = None
        super().__init__(type, ident, self.ret)


    def __repr__(self):
        return f"Function {self.ident}<{self.type}>({self.vl})"

    def new_local(self,local: Allocable):
        ev.alloc(local)
        self.locals.append(local)

    """
    To set params when the function is called
    """
    #@err.dangerous()
    def set_params(self,efpars):
        if len(efpars) != len(self.pm):
            return err.SCLFunArgsMismatchError(len(self.locals),len(efpars))
        for (i,tok) in enumerate(efpars):
            current_type = DT_TYPES.str_to_type(self.pm[i][0])
            current_idt  = self.pm[i][1]
            if tok.type == TokenType.VARRF:
                vr = ev.CURENV.prev_env.get_from_id(tok.value)
                if not vr.type == current_type and current_type != DT_TYPES.ANY:
                    return err.SCLWrongTypeError(current_type.name,vr.type.name)
                else:
                    if type(vr) is Array:
                        self.new_local(Array(vr.type,current_idt,vr.items))
                    else:
                        self.new_local(
                            Variable(VARKIND.MUT, current_type, current_idt, vr.get_value())
                        )
            else:
                if current_type == DT_TYPES.ANY:
                    if tok.type == TokenType.ARR:
                        self.new_local(
                            Array(DT_TYPES.ANY, current_idt, parser.parsing.eval_array_values(tok))
                        )
                    else:
                        self.new_local(
                            Variable(VARKIND.MUT, current_type, current_idt,
                                     DT_TYPES.guess_type(tok.value).convert_str_to_value(tok.value))
                        )
                elif current_type.get_literal_version() == tok.type:
                    self.new_local(
                        Variable(VARKIND.MUT,current_type,current_idt,current_type.convert_str_to_value(tok.value))
                    )
                else:
                    return err.SCLWrongTypeError(current_type.name, tok.type.name)

    def del_locals(self):
        for i in range(len(self.locals)):
            ev.de_alloc(self.locals.pop())
#TODO use regex to verify compatibility of string with values and in guessing the types
    def execute_fun(self,arguments: list[Token]):
        with Executor(environment=Environment()) as fexe:
            if self.pm != None:
                if (setpmerr := self.set_params(arguments)):
                    return setpmerr
            for ins in self.bd:
                fexe.execute(ins)
            if fexe.evm.fun_ret != None:
                if self.type == DT_TYPES.NIL:
                    return err.SCLNoReturnValueError(self.ident)
                elif self.type == DT_TYPES.ANY:
                    self.set_value(fexe.evm.fun_ret)
                elif self.type.is_compatible_with_type(str(fexe.evm.fun_ret)):
                    self.set_value(self.type.convert_str_to_value(str(fexe.evm.fun_ret)))
                else:
                    return err.SCLWrongReturnTypeError(self.ident,self.type.name,DT_TYPES.guess_type(fexe.evm.fun_ret).__repr__())
            else:
                self.set_value(self.type.default_value())
            self.del_locals()
            fexe.evm.fun_ret = None