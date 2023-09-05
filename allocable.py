from enum import Enum, auto

import ulang as ul
import env as ev
import TuiErrors as terr

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
class Allocable:

    def __init__(self, id:str, value):
        self.maddr = None
        self.id = id
        self.vl = value
        Allocable.alloc(self,self)

    def get_mem_addr(self):
        return self.maddr

    def alloc(cls, allocable):
        if (dup := ev.get_from_id(allocable.id)) == None:
            ev._VARS.append(allocable)
            allocable.maddr = ev._VARS.__len__() - 1
        else:
            print(f"'{allocable.id}' is already defined at address {dup.maddr}")

    def repr_val(self):
        return f"{self.vl}"

class Variable(Allocable):

    def __init__(self, type:DT_TYPES, id:str, value):
        self.type = type
        super().__init__(id, value)

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

    def convert_str_value_to_type(self,str_value:str):
        match self.type:
            case DT_TYPES.INT:
                return int(str_value)
            case DT_TYPES.FLT:
                return float(str_value)
            case DT_TYPES.STR:
                return str_value


    def __repr__(self):
        return f"Var<{self.type.__repr__()}>({self.id}:{self.vl})"

class Array(Allocable):

    def __init__(self, id:str, vars: list):
        super().__init__(id, vars)
        self.len = len(vars)

    def __repr__(self):
        out = f"Array<{self.id}>:["
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

    def __init__(self, id:str, params:list[str] | None, body:list[str]):
        self.pm = [] if params == None else params
        self.bd = body
        self.locals: list[Variable] = []
        self.ret = None
        super().__init__(id,self.ret)


    def __repr__(self):
        return f"Function:('{self.id}':{self.vl})"

    def init_params(self):
        for p in self.pm:
            temp = ul.parse(p)
            if (alen := len(temp)) == 2:
                self.locals.append(Variable(temp[0], temp[1], '0'))
            elif alen == 3:
                self.locals.append(Variable(temp[0], temp[1], ul.var_ref(temp[2])))

    """
    To set params when the function is called
    """
    def set_params(self,arguments: list[str]):
        if (loc_len := len(self.locals)) != (val_len := len(arguments)):
            terr.TuiFunArgsMismatchError(loc_len, val_len).trigger()
        for i in range(len(self.locals)):
            if arguments[i].startswith('$') and len(arguments[i]) > 1:
                if (arg_var := ev.get_from_id(arguments[i])) != None:
                    # TODO Fix Detecting type mismatch error when calling a function
                    pass
            self.locals[i].vl = ul.var_ref(arguments[i])

    def del_locals(self):
        for l in self.locals:
            ul.execute(f'del {l.id}')

    def execute_fun(self,arguments: list[str] | None):
        self.init_params()
        if self.pm != None:
            self.set_params(arguments)
        for ins in self.bd:
            if type(ins) is str:
                ul.execute(ins)
            else:
                ul.execute_block(ins)
        self.vl = ev._FUN_RET
        self.del_locals()
        ev._FUN_RET = None