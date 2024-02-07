from enum import Enum, auto
import re
from runtime import errors

BODY_PATTERN = re.compile(r"\{(?P<body_content>(?:.|\s)*)}")
PARAM_PATTERN = re.compile(r"\((?P<param_content>(?:.|\s)*)\)")
ARR_PATTERN = re.compile(r"\[(?P<arr_content>(?:.|\s)*)]")
STR_PATTERN = re.compile(r'<(?P<str_content>(?:.|\s)*)>')

#TODO Optional Tokens

class TokenType(Enum):
    ARG      = auto()
    BODY     = auto()
    PARAM    = auto()
    ARRAY    = auto()
    STRLIT   = auto()
    INTLIT   = auto()
    FLTLIT   = auto()
    BOOLLIT  = auto()
    VARREF   = auto()
    UNK      = -1

    def __repr__(self) -> str:
        match self.name:
            case 'ARG':
                return 'argument'
            case 'BODY':
                return 'body literal'
            case 'PARAM':
                return 'parameters literal'
            case 'ARRAY':
                return 'array literal'
            case 'STRLIT':
                return 'string'
            case 'INTLIT':
                return 'integer literal'
            case 'FLTLIT':
                return 'float literal'
            case 'BOOLLIT':
                return 'boolean literal'
            case 'VARREF':
                return 'variable reference'
            case 'UNK':
                return 'unknown token'
    def make_value(*token_types):
        return [TokenType.VARREF] + [t for t in token_types]

def all_literals():
    return (TokenType.INTLIT,TokenType.FLTLIT,TokenType.STRLIT,TokenType.BOOLLIT)

class ParseToken:
    def __init__(self,type: TokenType,value: str | list[str]):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"ParseToken:(type:'{self.type.__repr__()}';value:'{self.value}')"

    def has_specific_value(self, values: set):
        return self.value in values

def try_get(tokentypes:list[TokenType],position:int,args:list[ParseToken]) -> (ParseToken | None, errors.SCLError):
    #import errors  # avoid circular import
    if position >= len(args) :
        return (None,
                errors.SCLError(f"SyntaxError: missing token of type {[t.__repr__() for t in tokentypes]} at position {position + 2}"))
    if (wanted_token := args[position]).type not in tokentypes:
        return (None,
                errors.SCLError(f"SyntaxError: expected token of type {[t.__repr__() for t in tokentypes]} at position {position + 2}, got '{args[position].type.__repr__()}'"))
    else:
        return (wanted_token,None)

"""
When a command doesn't need arguments, only its head should be provided
"""
def no_extra_args(args: list[ParseToken]):
    if len(args) >= 1:
        return errors.SCLArgsMismatchError(extra=f"Extra arguments provided, please check the command syntax")
    return None


def parse_body(content: str, separator=';') -> list[str]:
    return re.split(f' *{separator} *',content)

def parse_param(content: str, separator=',') -> list[str]:
    return re.split(f' *{separator} *',content)

def parse_array(content: str, separator=',') -> list[str]:
    return re.split(f' *{separator} *',content)

def parse_formal_param(declaration: str):
    dec_parsed = parse(declaration)
    type_tok, err = try_get([TokenType.ARG],0,dec_parsed)
    if err:
        err.trigger()
    type: str = type_tok.value
    pname_tok, err = try_get([TokenType.ARG],1,dec_parsed)
    if err:
        err.trigger()
    pname: str = pname_tok.value
    return type,pname

def parse(inp_string: str) -> list[ParseToken]:
    #this splits elements with spaces not included in a "block"
    #a block is a scope delimited with { or ( or [ or < and their closing versions } ] ) >"
    command_parts = re.split(r" +(?![^\{\(\[<]*[\)\}\]>])", inp_string)
    tokens = []
    for p in command_parts:
        if BODY_PATTERN.fullmatch(p):
            tokens.append(ParseToken(TokenType.BODY,BODY_PATTERN.fullmatch(p).group('body_content')))
        elif PARAM_PATTERN.fullmatch(p):
            tokens.append(ParseToken(TokenType.PARAM,PARAM_PATTERN.fullmatch(p).group('param_content')))
        elif ARR_PATTERN.fullmatch(p):
            tokens.append(ParseToken(TokenType.ARRAY,ARR_PATTERN.fullmatch(p).group('arr_content')))
        elif STR_PATTERN.fullmatch(p):
            tokens.append(ParseToken(TokenType.STRLIT, STR_PATTERN.fullmatch(p).group('str_content')))
        elif (varref := re.fullmatch(r'\$[a-zA-Z_]\w*',p)):
            tokens.append(ParseToken(TokenType.VARREF,varref.group()[1:]))
        elif (intlit_mat := re.fullmatch(r'-?\d+',p)):
            tokens.append(ParseToken(TokenType.INTLIT, intlit_mat.group()))
            del intlit_mat
        elif (fltlit_mat := re.fullmatch(r'-?\d*\.\d+',p)):
            tokens.append(ParseToken(TokenType.FLTLIT, fltlit_mat.group()))
            del fltlit_mat
        elif (boollit_mat := re.fullmatch(r'true|false',p)):
            tokens.append(ParseToken(TokenType.BOOLLIT, boollit_mat.group()))
        elif (arg_mat := re.fullmatch(r'[a-zA-Z_]\w*',p)):
            tokens.append(ParseToken(TokenType.ARG,arg_mat.group()))
            del arg_mat
        else:
            tokens.append(ParseToken(TokenType.UNK,p))
    return tokens