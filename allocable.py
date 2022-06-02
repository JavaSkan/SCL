#Functions
import env as ev

class Allocable:

    def __init__(self, maddr, id:str, value):
        self.maddr = maddr
        self.id = id
        self.vl = value
        Allocable.alloc(self)

    def get_mem_addr(self):
        return self.maddr

    def alloc(cls, allocable):
        ev._VARS.append(allocable)
        allocable.maddr = ev._VARS.__len__()-1

    def repr_val(self):
        return f"{self.vl}"

class Variable(Allocable):

    def __init__(self, id:str, value):
        self.id = id
        self.vl = value
        super().alloc(self)

    def __repr__(self):
        return f"Var:({self.id}:{self.vl})"

class Array(Allocable):

    def __init__(self, id:str, vars: list[Variable]):
        self.id = id
        self.vl = vars
        self.len = len(vars)
        super().alloc(self)

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