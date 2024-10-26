from runtime import errors
from runtime.errors import dangerous
from .tokens import TokenType, Token
from .indexed import Indexed
from . import keywords

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

"""
Returns a list of length 2 that contains a type name and an identifier
"""
@dangerous(note="[PARSER-ERR] PARSING FORMAL PARAMETERS")
def check_formal_parameters(parameters: Token):
    res = []
    for parameter in parameters.value:
        if not parameter.type == TokenType.DECL:
            return errors.SCLInvalidFormalParameterError(parameter.type.__repr__())
        res.append([parameter.value[0].value,parameter.value[1].value])
    return res

"""
Parses Effective parameters, takes a tuple token <tok>
and returns the first parsed token of each part of the tuple
"""
@dangerous(note="[PARSER-ERR] PARSING EFFECTIVE PARAMETERS")
def check_effective_param(parameters: Token):
    res = []
    for parameter in parameters.value:
        if not parameter.type in {TokenType.INT, TokenType.FLT, TokenType.BOOL, TokenType.STR, TokenType.ARR,TokenType.VARRF}:
            return errors.SCLInvalidEffectiveParameterError(parameter.type.__repr__())
        res.append(parameter)
    return res

"""
tok: Should be of tokentype ARR
Converts array token to real python values
"""
def eval_array_values(tok: Token) -> list:
    res = []
    for vt in tok.value:
        res.append(vt.evaluate())
    return res

class Parser(Indexed):

    #TODO parse lines separated with ;
    def __init__(self, tokens: list[Token] = list) -> None:
        super().__init__(tokens)

    def parse_dec(self) -> Token:
        if not self.cur().has_specific_value(keywords.fml_prm_datatypes):
            errors.quick_err(tag="PARSER-ERR",msg=f"'{self.cur().value}' is not a valid type")
        content = [self.cur()]
        if self.has_next() and self.next().type == TokenType.IDT:
            self.advance()
            content.append(self.cur())
            return Token(TokenType.DECL,content)
        errors.quick_err(tag="PARSER-ERR",msg=f"Second part should be an argument token type")


    def parse_tuple(self) -> Token:
        content = []
        separated = False
        closed = False
        while self.has_next():
            self.advance()
            match self.cur().type:
                #literals
                case TokenType.INT | TokenType.FLT | TokenType.STR | TokenType.BOOL:
                    content.append(self.cur())
                #negative numbers
                case TokenType.MINUS:
                    rs = self.parse_neg()
                    if rs.type == TokenType.MINUS:
                        errors.quick_err(tag="PARSER-ERR",msg=f"Invalid Token For Tuple Content {self.cur()}")
                    content.append(rs)
                #parsing declaration
                case TokenType.IDT:
                    t = self.parse_dec()
                    if t.type == TokenType.IDT:
                        errors.quick_err(tag="PARSER-ERR",msg=f"Invalid Token For Tuple Content {self.cur()}")
                    content.append(t)
                #variable referencing
                case TokenType.DLR:
                    rs = self.parse_varref()
                    if rs.type == TokenType.DLR:
                        errors.quick_err(tag="PARSER-ERR" ,msg=f"Invalid Token For Tuple Content { self.cur()}")
                    content.append(rs)
                #arrays
                case TokenType.LBRK:
                    t = self.parse_arr()
                    content.append(t)
                case TokenType.CMA:
                    separated = True
                case TokenType.RPAR:
                    closed = True
                    break
                case _:
                    errors.quick_err(tag="PARSER-ERR",msg=f"Invalid Token For Tuple Content {self.cur()}")
            if self.has_next() and self.next().type != TokenType.CMA and self.next().type != TokenType.RPAR and not separated:
                errors.quick_err(tag="PARSER-ERR",msg=f"Missing a comma at position {self.ix + 1}")
            else:
                separated = False
        if closed:
            return Token(TokenType.TUPLE, content)
        else:
            errors.quick_err(tag="PARSER-ERR",msg=f"Right Parent Missing at position {self.ix + 1}")

    def parse_arr(self) -> Token:
        content = []
        separated = False
        closed = False
        while self.has_next():
            self.advance()
            match self.cur().type:
                #literals
                case TokenType.STR | TokenType.INT | TokenType.FLT | TokenType.BOOL:
                    content.append(self.cur())
                #negative numbers
                case TokenType.MINUS:
                    rs = self.parse_neg()
                    if rs.type == TokenType.MINUS:
                        errors.quick_err(tag="PARSER-ERR",msg=f"Invalid Token For Array Value {self.cur()}")
                    content.append(rs)
                #variable referencing
                case TokenType.DLR:
                    rs = self.parse_varref()
                    if rs.type == TokenType.DLR:
                        errors.quick_err(tag="PARSER-ERR", msg=f"Invalid Token For Array Value {self.cur()}")
                    content.append(rs)
                #arrays
                case TokenType.LBRK:
                    t = self.parse_arr()
                    content.append(t)
                case TokenType.CMA:
                    separated = True
                case TokenType.RBRK:
                    closed = True
                    break
                case _:
                    errors.quick_err(tag="PARSER-ERR", msg=f"Invalid Token {self.cur()}")
            if self.has_next() and self.next().type != TokenType.CMA and self.next().type != TokenType.RBRK and not separated:
                errors.quick_err(tag="PARSER-ERR", msg=f"Missing a comma at position {self.ix + 1}")
            else:
                separated = False
        if closed:
            return Token(TokenType.ARR, content)
        else:
            errors.quick_err(tag="PARSER-ERR", msg=f"Right Bracket Missing at position {self.ix + 1}")

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
            errors.quick_err(tag="PARSER-ERR", msg=f"Right Curly Bracket Missing at position {self.ix + 1}")

    def parse_varref(self) -> Token | None:
        if self.has_next() and self.next().type == TokenType.IDT:
            self.advance()
            return Token(TokenType.VARRF, self.cur().value)
        return None

    def parse_neg(self) -> Token | None:
        if self.has_next():
            if self.next().type == TokenType.INT:
                self.advance()
                return Token(TokenType.INT, '-' + self.cur().value)
            elif self.next().type == TokenType.FLT:
                self.advance()
                return Token(TokenType.FLT, '-' + self.cur().value)
        return None

    def parse_bool(self) -> Token | None:
        if self.cur().value == "true":
            return Token(TokenType.BOOL, self.cur().value)
        elif self.cur().value == "false":
            return Token(TokenType.BOOL, self.cur().value)
        else:
            return None #self.cur()

    def parse_bool_expr(self) -> Token | None:
        if self.cur().value == 'b' and self.has_next() and self.next().type == TokenType.STR:
            self.advance()
            return Token(TokenType.BLEXP, self.cur().value)
        else:
            return None

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
                    errors.quick_err(tag="PARSER-ERR", msg=f"Extra right parenthesis at pos {self.ix}")
                case TokenType.RBRK:
                    errors.quick_err(tag="PARSER-ERR", msg=f"Extra right bracket at position {self.ix}")
                case TokenType.RCBK:
                    errors.quick_err(tag="PARSER-ERR", msg=f"Extra right curly brakcet at position {self.ix}")
                case TokenType.DLR:
                    t = self.parse_varref() or Token(TokenType.DLR, self.cur().value)
                    res.append(t)
                case TokenType.MINUS:
                    t = self.parse_neg() or Token(TokenType.MINUS, self.cur().value)
                    res.append(t)
                case TokenType.IDT:
                    t = self.parse_bool() or self.parse_bool_expr() or Token(TokenType.IDT,self.cur().value)
                    res.append(t)
                case TokenType.SMCL:
                    break
                case _:
                    res.append(self.cur())
        return res

    def parse_lines(self) -> list[list[Token]]:
        lines = []
        while self.has_next():
            lines.append(self.parse())
            #self.advance()
        return lines