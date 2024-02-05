from enum import Enum, auto

from runtime import errors as err, env as ev
from runtime.ulang import var_ref_str, is_var_ref
from runtime.execution import execute, execute_block
#TODO create bool type and implement boolean system

#Enums
COUNT = 0

class DT_TYPES(Enum):

    INT = auto()
    FLT = auto()
    STR = auto()

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

    def str_to_type(str_type: str):
        match str_type:
            case 'int':
                return DT_TYPES.INT
            case 'flt':
                return DT_TYPES.FLT
            case 'str':
                return DT_TYPES.STR

class VARKIND(Enum):
    VAR = auto()
    CONST = auto()
    TEMP = auto()

    def str_to_varkind(str_kind: str):
        match str_kind:
            case "var":
                return VARKIND.VAR
            case "const":
                return VARKIND.CONST
            case "temp":
                return VARKIND.TEMP

class Allocable:

    def __init__(self, ident:str, value):
        self.maddr = None
        self.ident = ident
        self.vl = value
        Allocable.alloc(self,self)

    def get_mem_addr(self):
        return self.maddr

    def alloc(cls, allocable):
        if (dup := ev.get_from_id(allocable.ident)) == None:
            ev._VARS.append(allocable)
            allocable.maddr = ev._VARS.__len__() - 1
        else:
            print(f"'{allocable.ident}' is already defined at address {dup.maddr}")

    def repr_val(self):
        return f"{self.vl}"

class Variable(Allocable):

    #TODO implement variable kind temp
    def __init__(self, type:DT_TYPES, kind:VARKIND,ident:str, value):
        self.type = type
        self.kind = kind
        super().__init__(ident, value)

    def get_value(self):
        return self.vl

    def set_value(self,new):
        if self.kind == VARKIND.CONST:
            err.SCLModifyConstantError(self.ident).trigger()
        self.vl = new

    def is_compatible_with_type(self,str_value:str) -> bool:
        match self.type:
            case DT_TYPES.INT:
                return str_value.isdigit()
            case DT_TYPES.FLT:
                return str_value.replace('.','',1).isdigit()
            case DT_TYPES.STR:
                return True

    def convert_str_value_to_type(self,str_value:str):
        match self.type:
            case DT_TYPES.INT:
                return int(str_value)
            case DT_TYPES.FLT:
                return float(str_value)
            case DT_TYPES.STR:
                return str_value


    def __repr__(self):
        return f"Var<{self.type.__repr__()}>({self.ident}:{self.vl})"

class Array(Allocable):

    def __init__(self, ident:str, vars: list):
        super().__init__(ident, vars)
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

    def __init__(self, ident:str, params:list[str] | None, body:list[str]):
        self.pm = [] if params == None else params
        self.bd = body
        self.locals: list[Variable] = []
        self.ret = None
        super().__init__(ident,self.ret)


    def __repr__(self):
        return f"Function:('{self.ident}':{self.vl})"

    def init_params(self):
        for p in self.pm:
            temp = None #TODO parse(p)
            if (alen := len(temp)) == 2:
                self.locals.append(Variable(DT_TYPES.str_to_type(temp[0]), temp[1], None))
            elif alen == 3:
                self.locals.append(Variable(DT_TYPES.str_to_type(temp[0]), temp[1], var_ref_str(temp[2])))

    """
    To set params when the function is called
    """
    def set_params(self,arguments: list[str]):
        if (loc_len := len(self.locals)) != (val_len := len(arguments)):
            err.SCLFunArgsMismatchError(loc_len, val_len).trigger()
        for i in range(len(self.locals)):
            if (arg_var := (ev.get_from_id(arguments[i][1:]) if is_var_ref(arguments[i]) else arguments[i])) == None:
                err.SCLNotFoundError(arguments[i]).trigger()
            if type(arg_var) is str:
                if self.locals[i].is_compatible_with_type(arg_var):
                    self.locals[i].set_value(self.locals[i].convert_str_value_to_type(arg_var))
                else:
                    err.SCLWrongTypeError(self.locals[i].type.__repr__()).trigger()
            else:
                if self.locals[i].is_compatible_with_type(str(arg_var.get_value())):
                    self.locals[i].set_value(arg_var.get_value())
                else:
                    err.SCLWrongTypeError(self.locals[i].type.__repr__(),arg_var.type.__repr__()).trigger()

    def del_locals(self):
        for l in self.locals:
            execute(f'del {l.ident}')

    def execute_fun(self,arguments: list[str] | None):
        self.init_params()
        if self.pm != None:
            self.set_params(arguments)
        for ins in self.bd:
            if type(ins) is str:
                execute(ins)
            else:
                execute_block(ins)
        self.vl = ev._FUN_RET
        self.del_locals()
        ev._FUN_RET = None