#Functions
import env as ev

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

    def __init__(self, id:str, value):
        super().__init__(id, value)

    def __repr__(self):
        return f"Var:({self.id}:{self.vl})"

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