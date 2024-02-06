from enum import Enum, auto

from runtime import errors as err, env as ev
from runtime.ulang import var_ref_str, is_var_ref
from runtime.execution import execute, execute_block
from parser.parsing import parse_formal_param
#TODO implement boolean system

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

    def is_compatible_with_type(self,str_value:str) -> bool:
        match self.type:
            case DT_TYPES.INT:
                return str_value.isdigit()
            case DT_TYPES.FLT:
                return str_value.replace('.','',1).isdigit()
            case DT_TYPES.STR:
                return True
            case DT_TYPES.BOOL:
                return str_value == 'true' or str_value == 'false'

    def convert_str_value_to_type(self,str_value:str):
        match self.type:
            case DT_TYPES.INT:
                return int(str_value)
            case DT_TYPES.FLT:
                return float(str_value)
            case DT_TYPES.STR:
                return str_value
            case DT_TYPES.BOOL:
                return str_value == 'true'

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

    def __init__(self, type:DT_TYPES,ident:str, params:list[str] | None, body:list[str]):
        self.pm = [] if params == None else params
        self.bd = body
        self.locals = []
        self.ret = None
        super().__init__(type, ident, self.ret)


    def __repr__(self):
        return f"Function:('{self.ident}':{self.vl})"

    def init_params(self):
        for p in self.pm:
            type,name = parse_formal_param(p)
            self.locals.append(Variable(VARKIND.MUT,DT_TYPES.str_to_type(type),name,None))
            ev.alloc(self.locals[len(self.locals)-1])

    """
    To set params when the function is called
    """
    def set_params(self,arguments: list[str]):
        if len(arguments) != len(self.locals):
            err.SCLFunArgsMismatchError(len(self.locals),len(arguments)).trigger(note=f"arguments provided: {str(arguments)}")
        for (i,arg) in enumerate(arguments):
            if is_var_ref(arg):
                if not (var := ev.get_from_id(arg[1:])):
                    err.SCLNotFoundError(arg[1:])
                if not var.type == self.locals[i].type:
                    err.SCLWrongTypeError(self.locals[i].type.__repr__())
                self.locals[i].set_value(var.get_value())
            else:
                if self.locals[i].is_compatible_with_type(arg):
                    self.locals[i].set_value(self.locals[i].convert_str_value_to_type(arg))

    def del_locals(self):
        self.locals.clear()

    #arguments are var refs or literals ($x or 0 ...)
    def execute_fun(self,arguments: list[str]):
        self.init_params()
        if self.pm != None:
            self.set_params(arguments)
        for ins in self.bd:
            execute(ins)
        if ev._FUN_RET:
            if self.is_compatible_with_type(ev._FUN_RET):
                self.set_value(self.convert_str_value_to_type(ev._FUN_RET))
            else:
                return err.SCLWrongReturnTypeError(self.ident,self.type.__repr__(),DT_TYPES.guess_type(ev._FUN_RET).__repr__())
        else:
            self.set_value(self.type.default_value())
        self.del_locals()
        ev._FUN_RET = None