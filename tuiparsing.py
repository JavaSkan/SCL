from enum import Enum, auto
import re

#OVERALL_PATTERN = re.compile(r"(?P<args>(?:[a-z]+ ?)+) ?(?:\((?P<param_content>.*)\))? *(?:\{(?P<body_content>.*)\})?$")
BODY_PATTERN = re.compile(r"\{(?P<body_content>(?:.|\s)*)}")
PARAM_PATTERN = re.compile(r"\((?P<param_content>(?:.|\s)*)\)")
ARR_PATTERN = re.compile(r"\[(?P<arr_content>(?:.|\s)*)]")
STR_PATTERN = re.compile(r'<(?P<str_content>(?:.|\s)*)>')

class TokenType(Enum):
    ARG   = auto()
    BODY  = auto()
    PARAM = auto()
    ARRAY = auto()
    STR   = auto()
    INT   = auto()
    FLT   = auto()
    UNK   = -1

    def __repr__(self):
        return self.name
class ParseToken:
    def __init__(self,type: TokenType,value: str | list[str]):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"ParseToken:(type:'{self.type.__repr__()}';value:{self.value})"

# def try_get(tokentype:TokenType,position:int,args:list[ParseToken]):
#     import tuierrors #avoid circular import
#     if position >= len(args):
#         return tuierrors.TuiError(f"SyntaxError: There is no argument at {position} (command arguments length = {len(args)})").trigger()
#     if (wanted_token := args[position]).type != tokentype:
#         return tuierrors.TuiError(f"SyntaxError: expected {tokentype.__repr__()} at {position} and found {args[position].type.__repr__()}").trigger()
#     else:
#         return wanted_token

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
            tokens.append(ParseToken(TokenType.STR,STR_PATTERN.fullmatch(p).group('str_content')))
        elif (arg_mat := re.fullmatch(r'[a-zA-Z_@]\w*',p)):
            tokens.append(ParseToken(TokenType.ARG,arg_mat.group()))
            del arg_mat
        elif (intlit_mat := re.fullmatch(r'\d+',p)):
            tokens.append(ParseToken(TokenType.INT,intlit_mat.group()))
            del intlit_mat
        elif (fltlit_mat := re.fullmatch(r'\d*\.\d+',p)):
            tokens.append(ParseToken(TokenType.FLT,fltlit_mat.group()))
            del fltlit_mat
        else:
            tokens.append(ParseToken(TokenType.UNK,p))
    return tokens