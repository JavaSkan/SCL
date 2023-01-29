import ulang as ul
import env as ev

#Enums
COUNT = 0

def iota():
    global COUNT
    COUNT += 1
    return COUNT

def iota_limit():
    global COUNT
    COUNT = -1

class DT_TYPES:

    iota_limit()
    INT = iota()
    FLT = iota()
    STR = iota()
    iota_limit()


    TYPES = {
        "int":INT,
        "flt":FLT,
        "str":STR
    }

    NUMBERS = [
        INT,
        FLT
    ]

    def repr(cls,dtt):
         match cls.TYPES[dtt]:
             case 0:
                 return "integer"
             case 1:
                 return "float"
             case 2:
                 return "string"

class Allocable:

    def __init__(self, id:str, value):
        self.maddr = None
        self.id = id
        self.vl = value
        Allocable.alloc(self,self)

    def get_mem_addr(self):
        return self.maddr

    def alloc(cls, allocable):
        dup = ev.get_from_id(allocable.id)
        if dup == None:
            ev._VARS.append(allocable)
            allocable.maddr = ev._VARS.__len__() - 1
        else:
            print(f"'{allocable.id}' is already defined at address {dup.maddr}")

    def repr_val(self):
        return f"{self.vl}"

class Variable(Allocable):

    def __init__(self, type:str, id:str, value:str):
        self.type = type
        super().__init__(id, value)

    def get_value(self):
        match DT_TYPES.TYPES.get(self.type):
            case 0:
                return int(self.vl)
            case 1:
                return float(self.vl)
            case 2:
                return self.vl
            case _:
                return self.vl

    def __repr__(self):
        return f"Var:({self.id}<{DT_TYPES.repr(DT_TYPES,self.type)}>:{self.vl})"

class Array(Allocable):

    def __init__(self, id:str, vars: list[Variable]):
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

    def rem_v(self,idx):
        return self.vl.pop(idx)

class Function(Allocable):

    def __init__(self, id:str, body: list):
        self.bd = body
        self.ret = None
        super().__init__(id,self.ret)


    def __repr__(self):
        return f"Function:({self.id}:{self.vl})"

    def execute_fun(self):
        for ins in self.bd:
            if type(ins) is str:
                ul.execute(ins)
            else:
                ul.execute_block(ins)
        self.vl = ev._FUN_RET
        ev._FUN_RET = None