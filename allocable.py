#Functions
import ulang as u

class MemData:
    def __init__(self,index,value):
        self.index = index
        self.value = value

    def __repr__(self):
        return f'{self.index} : {self.value}'


class Memory:

    def __init__(self):
        self.elements: MemData = []
        self.index = 0

    def get_at(self,pos):
        return self.elements[pos if pos < self.elements.__len__ else self.elements.__len__]

    def allocate(self,value):
        self.elements.append(MemData(self.index,value))
        self.index += 1

    def delete(self,pos):
        self.elements.pop(pos)

    def get_value(self,pos):
        return self.get_at(pos).value

class AFunction(MemData):
    def __init__(self,id,insts):
        self.id = id
        self.insts = insts
        MemData.__init__(self)

class AVariable(MemData):
    def __init__(self,id,value):
        self.id = id
        self.value = value