from typing import Any

class Indexed:
    def __init__(self, inp: Any) -> None:
        self.inp = inp
        self.ix = -1

    def reset(self,new: Any = None) -> None:
        if new != None:
            self.inp = new
        self.ix = -1

    def cur(self) -> Any:
        return self.inp[self.ix]

    def has_next(self) -> bool:
        return self.ix < len(self.inp) - 1

    def advance(self) -> None:
        if self.has_next():
            self.ix += 1

    def back(self) -> None:
        if self.ix > 0:
            self.ix -= 1

    def next(self) -> Any:
        # self.advance()
        return self.inp[self.ix + 1]

    """def check_next(self,c) -> bool:
        return self.cur() == c and self.has_next()"""