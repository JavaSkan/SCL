from enum import Enum, auto

from runtime import errors as err, env as ev
from runtime.execution import execute
from parser.parsing import TokenType, Token, parse_formal_params, parse_effective_param
#TODO implement boolean system
#TODO create a class called iterable as a mother-class of a string variable and arrays

class DT_TYPES(Enum):

    INT  = auto()
    FLT  = auto()
    STR  = auto()
    BOOL = auto()

    def __repr__(self):
        return self.to_python_type().__class__.__name__

    def to_python_type(self):
        match self:
            case DT_TYPES.INT:
                return int()
            case DT_TYPES.FLT:
                return float()
            case DT_TYPES.STR:
                return str()
            case DT_TYPES.BOOL:
                return bool()

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

    def guess_type(str_value: str):
        if str_value.isdigit():
            return DT_TYPES.INT
        elif str_value.replace('.','',1).isdigit():
            return DT_TYPES.FLT
        elif str_value == 'true' or str_value == 'false':
            return DT_TYPES.BOOL
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

    def convert_str_to_value(self,str_value):
        match self:
            case DT_TYPES.INT:
                return int(str_value)
            case DT_TYPES.FLT:
                return float(str_value)
            case DT_TYPES.STR:
                return str_value
            case DT_TYPES.BOOL:
                return str_value == 'true'

    def is_compatible_with_type(self,str_value):
        match self:
            case DT_TYPES.INT:
                return str_value.isdigit() or str_value.startswith('-') and str_value[1:].isdigit()
            case DT_TYPES.FLT:
                return (p := str_value.replace('.', '', 1)).isdigit() or p.startswith('-') and p[1:].isdigit()
            case DT_TYPES.STR:
                return True
            case DT_TYPES.BOOL:
                return str_value == 'true' or str_value == 'false'

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

class Allocable:

    def __init__(self, type: DT_TYPES, ident:str, value):
        self.maddr = None
        self.type = type
        self.ident = ident
        self.vl = value

    def get_value(self):
        return self.vl

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
        return f"Var<{self.kind.__repr__()} {self.type.__repr__()}>({self.ident}:{self.vl})"

class Array(Allocable):

    def __init__(self, type: DT_TYPES,ident:str, vars: list):
        super().__init__(type, ident, vars)
        self.len = len(vars)

    def __repr__(self):
        out = f"Array<{self.ident}>:["
        for i in range(self.len-1):
            out += f"{self.vl[i]},"
        out += f"{self.vl[len(self.vl)-1]}]"
        return out

    def get_v(self,idx):
        return self.vl[idx]

    def add_v(self,var:Variable):
        self.vl.append(var)

    #TODO find a way to use this function
    def rem_v(self,idx):
        return self.vl.pop(idx)

class Function(Allocable):

    def __init__(self, type:DT_TYPES,ident:str, params:list[Token] | None, body:list[str]):
        self.pm = [] if params == None else params
        self.bd = body
        self.locals = []
        self.ret = None
        super().__init__(type, ident, self.ret)


    def __repr__(self):
        return f"Function:('{self.ident}':{self.vl})"

    def init_params(self):
        for p in self.pm:
            type,name = parse_formal_params(p)
            self.locals.append(Variable(VARKIND.MUT,DT_TYPES.str_to_type(type),name,None))
            ev.alloc(self.locals[len(self.locals)-1])

    """
    To set params when the function is called
    """
    def set_params(self,efpars):
        if len(efpars) != len(self.locals):
            return err.SCLFunArgsMismatchError(len(self.locals),len(efpars))
        for (i,e) in enumerate(efpars):
            tok = e
            if tok.type == TokenType.VARRF:
                vr = ev.get_from_id(tok.value)
                if not vr.type == self.locals[i].type:
                    err.SCLWrongTypeError(self.locals[i].type.__repr__(),vr.type.__repr__()).trigger()
                else:
                    self.locals[i].set_value(self.locals[i].type.convert_str_to_value(vr.vl))
            else:
                if not self.locals[i].type.get_literal_version() == tok.type:
                    err.SCLWrongTypeError(self.locals[i].type.__repr__(),tok.type.__repr__()).trigger()
                else:
                    self.locals[i].set_value(self.locals[i].type.convert_str_to_value(tok.value))




    def del_locals(self):
        for local in self.locals:
            ev.de_alloc(local)

    #arguments are var refs or literals ($x or 0 ...)
    def execute_fun(self,arguments: list[Token]):
        self.init_params()
        if self.pm != None:
            if (setpmerr:=self.set_params(arguments)):
                return setpmerr
        for ins in self.bd:
            execute(ins)
        if ev._FUN_RET:
            if self.type.is_compatible_with_type(ev._FUN_RET):
                self.set_value(self.type.convert_str_to_value(ev._FUN_RET))
            else:
                return err.SCLWrongReturnTypeError(self.ident,self.type.__repr__(),DT_TYPES.guess_type(ev._FUN_RET).__repr__())
        else:
            self.set_value(self.type.default_value())
        self.del_locals()
        ev._FUN_RET = None