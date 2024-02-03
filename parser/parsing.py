from enum import Enum, auto
import re
import errors

BODY_PATTERN = re.compile(r"\{(?P<body_content>(?:.|\s)*)}")
PARAM_PATTERN = re.compile(r"\((?P<param_content>(?:.|\s)*)\)")
ARR_PATTERN = re.compile(r"\[(?P<arr_content>(?:.|\s)*)]")
STR_PATTERN = re.compile(r'<(?P<str_content>(?:.|\s)*)>')


class TokenType(Enum):
    ARG      = auto()
    BODY     = auto()
    PARAM    = auto()
    ARRAY    = auto()
    STRLIT   = auto()
    INTLIT   = auto()
    FLTLIT   = auto()
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
            case 'VARREF':
                return 'variable reference'
            case 'UNK':
                return 'unknown token'

class ParseToken:
    def __init__(self,type: TokenType,value: str | list[str]):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"ParseToken:(type:'{self.type.__repr__()}';value:{self.value})"

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

def parse_body(content: str, separator=';') -> list[str]:
    return re.split(f' *{separator} *',content)

def parse_param(content: str, separator=',') -> list[str]:
    return re.split(f' *{separator} *',content)

def parse_array(content: str, separator=',') -> list[str]:
    return re.split(f' *{separator} *',content)


def parse(inp_string: str) -> list[ParseToken]:
    #this splits elements with spaces not included in a "block"
    #a block is a scope delimited with { or ( or [ " and their closing versions } ] ) "
    command_parts = re.split(r" +(?![^{([<]*[\)\}\]>])", inp_string)
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
        elif (arg_mat := re.fullmatch(r'[a-zA-Z_]\w*',p)):
            tokens.append(ParseToken(TokenType.ARG,arg_mat.group()))
            del arg_mat
        elif (varref := re.fullmatch(r'\$\w+',p)):
            tokens.append(ParseToken(TokenType.VARREF,varref.group()[1:]))
        elif (intlit_mat := re.fullmatch(r'\d+',p)):
            tokens.append(ParseToken(TokenType.INTLIT, intlit_mat.group()))
            del intlit_mat
        elif (fltlit_mat := re.fullmatch(r'\d*\.\d+',p)):
            tokens.append(ParseToken(TokenType.FLTLIT, fltlit_mat.group()))
            del fltlit_mat
        else:
            tokens.append(ParseToken(TokenType.UNK,p))
    return tokens