from enum import Enum, auto


class TokenType(Enum):
    # General Token Types
    UNK = -1
    ARG = auto()  # identifier

    # Datatypes
    INT = auto()  # integer
    FLT = auto()  # float
    STR = auto()  # string literal
    BOOL = auto()  # boolean literal

    # Scope Characters Opening(L) / Closing(R)
    LPAR = auto()  # left  parenthesis   (
    RPAR = auto()  # right parenthesis   )
    LBRK = auto()  # left  brakcet       [
    RBRK = auto()  # right bracket       ]
    LCBK = auto()  # left  curly bracket {
    RCBK = auto()  # right curly bracket }

    # Special Characters
    AT = auto()  # at           @
    DLR = auto()  # dollar sign  $
    DQT = auto()  # double quote "

    # Punctuation Characters
    CLN = auto()  # colon     :
    SMCL = auto()  # semicolon ;
    CMA = auto()  # comma     ,
    DOT = auto()  # colon     .

    # Arithmetic Characters
    PLUS = auto()  # plus           +
    MINUS = auto()  # minux          -
    STAR = auto()  # star/mult      *
    SLASH = auto()  # slash/div      /
    PERCT = auto()  # percent/modulo %

    # Scope Token Types
    BODY = auto()  # Body scope         {...}
    TUPLE = auto()  # Tuple              (...)
    ARR = auto()  # Array literal      [...]
    VARRF = auto()  # Variable reference $<IDT>

    def __repr__(self) -> str:
        return self.name


class Token:

    def __init__(self, type: TokenType, value: str | list) -> None:
        self.type = type
        self.value = value

    def __repr__(self) -> str:
        """v = '\n'
        if self.t in {TokenType.ARR,TokenType.BODY,TokenType.TUPLE}:
            for e in self.v:
                v += f"\t{' '.join([t.__repr__() for t in e])}\n"
            return f"{self.t.__repr__()}:[{v}]"""
        return f"{self.type.__repr__()}:'{self.value}'"

    def has_specific_value(self,values) -> bool:
        return self.value in values

    def is_empty_tuple(self) -> bool:
        if self.type == TokenType.TUPLE:
            return len(self.value) == 1 and len(self.value[0]) == 0
        return False

    def evaluate(self):
        match self.type:
            case TokenType.INT:
                return int(self.value)
            case TokenType.FLT:
                return float(self.value)
            case TokenType.STR:
                return self.value
            case TokenType.BOOL:
                return self.value == 'true' or not (self.value == 'false')
            case _:
                return self

def all_literals():
    return {
        TokenType.INT,
        TokenType.FLT,
        TokenType.STR,
        TokenType.BOOL
    }
