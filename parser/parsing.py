from runtime import errors
from runtime.errors import dangerous
from .tokens import TokenType, Token
from .indexed import Indexed
from . import keywords

def make_value(*token_types):
    return [TokenType.VARRF] + [t for t in token_types]

@dangerous(note="[PARSING] TOKEN MISMATCH")
def try_get(tokentypes:list[TokenType], position:int, args:list[Token]) -> (Token | None, errors.SCLError):
    #import errors  # avoid circular import
    if position >= len(args) :
        return errors.SCLError(f"SyntaxError: missing token of type '{' | '.join([t.__repr__() for t in tokentypes])}' at position {position + 2}")
    if (wanted_token := args[position]).type not in tokentypes:
        return errors.SCLError(f"SyntaxError: expected token of type '{' | '.join([t.__repr__() for t in tokentypes])}' at position {position + 2}, got '{args[position].type.__repr__()}'")
    else:
        return wanted_token

"""
When a command doesn't need arguments, only its head should be provided
"""
def no_extra_args(args: list[Token]):
    if len(args) >= 1:
        return errors.SCLArgsMismatchError(extra=f"Extra arguments provided, please check the command syntax")
    return None

@dangerous(note="[PARSER-ERR] PARSING FORMAL PARAMETERS")
def parse_formal_params(args: list[Token]) -> (str,str):
    if len(args) == 0:
        return ("","")
    type_tok: Token = try_get([TokenType.ARG],0,args)
    if not type_tok.has_specific_value(keywords.data_types_keywords):
        return errors.SCLUnknownTypeError(type_tok.value)
    name_tok: Token = try_get([TokenType.ARG], 1, args)
    return type_tok.value,name_tok.value

"""
Parses Effective parameters, takes a tuple token <tok>
and returns the first parsed token of each part of the tuple
"""
def parse_effective_param(tok: Token) -> list[Token]:
    res = []
    p = Parser([])
    for toks in tok.value:
        p.reset(toks)
        if len(toks) == 0:
            continue
        res.append(p.parse()[0])
    return res

"""
Parses arrays values into real python values
"""
def parse_array_values(tok: Token) -> list:
    res = []
    p = Parser([])
    for toks in tok.value:
        p.reset(toks)
        if len(toks) == 0:
            continue
        res.append(p.parse()[0].evaluate())
    return res

class Parser(Indexed):

    def __init__(self, tokens: list[Token]) -> None:
        super().__init__(tokens)

    def parse_tuple(self) -> Token:
        content = []
        buf = []
        closed = False
        while self.has_next():
            self.advance()
            match self.cur().type:
                case TokenType.LPAR:
                    t = self.parse_tuple()
                    buf.append(t)
                case TokenType.CMA:
                    content.append(buf.copy())
                    buf.clear()
                case TokenType.RPAR:
                    closed = True
                    break
                case _:
                    buf.append(self.cur())
        if closed:
            content.append(buf.copy())
            return Token(TokenType.TUPLE, content)
        else:
            print("Right Parent Missing at", self.ix + 1)
            quit()

    def parse_arr(self) -> Token:
        content = []
        buf = []
        closed = False
        while self.has_next():
            self.advance()
            match self.cur().type:
                case TokenType.LBRK:
                    t = self.parse_arr()
                    buf.append(t)
                case TokenType.CMA:
                    content.append(buf.copy())
                    buf.clear()
                case TokenType.RBRK:
                    closed = True
                    break
                case _:
                    buf.append(self.cur())
        if closed:
            content.append(buf.copy())
            return Token(TokenType.ARR, content)
        else:
            print("Right Bracket Missing at", self.ix + 1)
            quit()

    def parse_body(self) -> Token:
        content = []
        buf = []
        closed = False
        while self.has_next():
            self.advance()
            match self.cur().type:
                case TokenType.LCBK:
                    t = self.parse_body()
                    buf.append(t)
                case TokenType.SMCL:
                    content.append(buf.copy())
                    buf.clear()
                case TokenType.RCBK:
                    closed = True
                    break
                case _:
                    buf.append(self.cur())
        if closed:
            content.append(buf.copy())
            return Token(TokenType.BODY, content)
        else:
            print("Right Curly Bracket Missing at", self.ix + 1)
            quit()

    def parse_varref(self) -> Token:
        if self.has_next() and self.next().type == TokenType.ARG:
            self.advance()
            return Token(TokenType.VARRF, self.cur().value)
        return Token(TokenType.DLR, self.cur().value)

    def parse_neg(self) -> Token:
        if self.has_next():
            if self.next().type == TokenType.INT:
                self.advance()
                return Token(TokenType.INT, '-' + self.cur().value)
            elif self.next().type == TokenType.FLT:
                self.advance()
                return Token(TokenType.FLT, '-' + self.cur().value)
        return Token(TokenType.MINUS, self.cur().value)

    def parse_bool(self) -> Token:
        if self.cur().value == "true":
            return Token(TokenType.BOOL, self.cur().value)
        elif self.cur().value == "false":
            return Token(TokenType.BOOL, self.cur().value)
        else:
            return self.cur()

    def parse(self) -> list[Token]:
        res = []
        while self.has_next():
            self.advance()
            match self.cur().type:
                case TokenType.LPAR:
                    t = self.parse_tuple()
                    res.append(t)
                case TokenType.LBRK:
                    t = self.parse_arr()
                    res.append(t)
                case TokenType.LCBK:
                    t = self.parse_body()
                    res.append(t)
                case TokenType.RPAR:
                    print("Extra right parenthesis at pos", self.ix)
                    quit()
                case TokenType.RBRK:
                    print("Extra right bracket at position", self.ix)
                    quit()
                case TokenType.RCBK:
                    print("Extra right curly brakcet at position", self.ix)
                    quit()
                case TokenType.DLR:
                    t = self.parse_varref()
                    res.append(t)
                case TokenType.MINUS:
                    t = self.parse_neg()
                    res.append(t)
                case TokenType.ARG:
                    t = self.parse_bool()
                    res.append(t)
                case _:
                    res.append(self.cur())
        return res