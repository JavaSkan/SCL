#Functions
import env as ev

class Allocable:

    def __init__(self, maddr):
        self.maddr = maddr
        self.alloc()

    def get_mem_addr(self):
        return self.maddr

    def alloc(self):
        ev._VARS.append(self)
        self.maddr = ev._VARS.__len__()-1

class Variable(Allocable):

    def __init__(self, id:str, value):
        self.id = id
        self.vl = value
        super().alloc()

    def __repr__(self):
        return f"Var:({self.id}:{self.vl})"

class Array(Allocable):

    def __init__(self, id:str, vars: list[Variable]):
        self.id = id
        self.vars = vars
        self.len = vars.__len__()
        super().alloc()

    def __repr__(self):
        out = f"Array<{self.id}>:["
        for i in range(self.len):
            out += f"{self.vars[i]}"
        out += "]"
        return out

    def get_v(self,idx):
        return self.vars[idx]

    def rem_v(self,idx):
        return self.vars.pop(idx)