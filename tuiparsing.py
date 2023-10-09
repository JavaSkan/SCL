from enum import Enum, auto
#import TuiErrors
OPENING_CHARS = '{[("'
CLOSING_CHARS = '}])"'

class TokenType(Enum):
    ARG  =  auto()
    BODY =  auto()
    PARAM = auto()
    ARRAY = auto()
    STR   = auto()

    def __repr__(self):
        return self.name
class ParseToken:
    def __init__(self,type: TokenType,value: str | list[str]):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"ParseToken:(type:'{self.type.__repr__()}';value:{self.value})"

# def try_get(tokentype:TokenType,position:int,args:list[ParseToken]):
#     if position >= len(args):
#         TuiErrors.TuiError(f"SyntaxError: There is no argument at {position} (command arguments length = {len(args)})").trigger()
#         return # In case ERR_QUIT is set to false
#     if (wanted_token := args[position]).type != tokentype:
#         TuiErrors.TuiError(f"SyntaxError: wanted {tokentype.__repr__()} at {position} and found {args[position].type.__repr__()}").trigger()
#         return # In case ERR_QUIT is set to false
#     else:
#         return wanted_token

"""
Char Positions in a String
"""
def cpos(inp: str, c) -> list:
    return [i for i,v in enumerate(inp) if v == c]

def is_not_in_block(inp: str, pos: int, copen: str, cclose: str) -> bool:
    open_positions = cpos(inp, copen)
    close_positions = cpos(inp, cclose)
    open_positions.sort()
    close_positions.sort()
    return open_positions[0] > pos < close_positions[-1]


"""
<copen> being the character of opening (ex: {)
<cclose> being the character of closing (ex: })

stands for binary partition, parsing to two sides
side1 "element" side2
"""
def parse_binp(inp: str, c: str, copen: str, cclose: str) -> list:
    res = []
    sc_pos = cpos(inp, c)

    lposs = cpos(inp, copen)
    rposs = cpos(inp, cclose)

    #if there is no <copen> or <cclose> or delimiter characters are not matching then it returns the whole split string
    if (lposs == [] or rposs == []) or len(lposs) != len(rposs):
        return inp.split(c) if c != "" else [inp]

    lpos = lposs[0]
    rpos = rposs[-1]

    prev_sc_pos = 0
    del lposs, rposs

    for i in range(len(sc_pos)):
        #checks if <c> is not included in a block delimited with <copen> and <cclose>
        if sc_pos[i] < lpos or sc_pos[i] > rpos:
            res.append(inp[prev_sc_pos:sc_pos[i]])
            prev_sc_pos = sc_pos[i]+1
    res.append(inp[prev_sc_pos:len(inp)])
    return res

"""
Parses a delimited chunk in the script (inp)
<block_char_open>: opening delimiter
<block_char_closing>: closing delimiter
<binop_char>: to parse what's in the block
"""
#TODO Replace raising exceptions with TuiErrors + replacing message by 'one extra closing/opening character' at pos <pos>
def parse_block(inp: str, block_char_open: str, block_char_close: str, binop_char: str):
    lpos = cpos(inp,block_char_open)
    rpos = cpos(inp,block_char_close)

    if lpos == [] or rpos == []:
        return inp
    elif (lft_pl := len(lpos)) > (rgt_pl := len(rpos)):
        raise Exception(f"Missing {block_char_close} after the last one at position {rpos[rgt_pl-1]}")
    elif lft_pl < rgt_pl:
        raise Exception(f"Missing {block_char_open} before the first one at position {lpos[0]}")

    #inp but without delimiters ('{' or '}' for ex)
    res = parse_binp(inp[lpos[0]+1:rpos[-1]],binop_char,block_char_open,block_char_close)

    for i in range(len(res)):
        #idk why it doesn't work with strip(), that's why i do it manually
        while res[i].startswith(' '):
            res[i] = res[i][1:]
        while res[i].endswith(' '):
            res[i] = res[i][:-1]
        if res[i].startswith(block_char_open) and res[i].endswith(block_char_close):
            res[i] = parse_block(res[i],block_char_open,block_char_close,binop_char)
    return res

def parse_body(inp: str) -> ParseToken:
    return ParseToken(TokenType.BODY,parse_block(inp,'{','}',';'))

def parse_arr(inp) -> ParseToken:
    return ParseToken(TokenType.ARRAY,parse_block(inp,'[',']',','))

def parse_params(inp) -> ParseToken:
    return ParseToken(TokenType.PARAM,parse_block(inp,'(',')',','))

"""
=> Parses The First String Literal Expression It Finds In The Input String

! Effective string parameter must start at the location of the first (")
for example: 
start_string = 'string s = "Hello World"'
s (parameter) = '"Hello World"'

! Returns a tuple containing the parsed string AND a int value which is the end of the string
literal expression, which is the character (")
"""
def parse_str_literal(s:str) -> (ParseToken,int):
    closing_char_pos = s[1:].find('"')
    if closing_char_pos != -1:
        return ParseToken(TokenType.STR,s[1:closing_char_pos+1]),closing_char_pos
    #TuiErrors.TuiError(f"Syntax Error: forgot to close string literal expression in '{s}'").trigger()

"""
If plenty of STR Tokens are aside of each other in a given list of ParseTokens, they with get grouped in one single STR Token
"""
def parse_group_str(tokens: list[ParseToken]):
    i = 0
    string_buf = ''
    while i < len(tokens):
        if tokens[i].type == TokenType.STR:
            while tokens[i].type == TokenType.STR and i < len(tokens):
                string_buf += tokens[i].value
                tokens.pop(i)
            tokens.insert(i,ParseToken(TokenType.STR, string_buf))
            string_buf = ''
        i += 1
def parse_tokens(s:str) -> list[ParseToken]:
    buf = ''
    openings = 0
    fst_open = ''
    lst_close = ''
    goto_index = 0 #used when forming strings
    res = []
    for i, v in enumerate(s):
        if i < goto_index:
            continue #To skip characters included in string
        if v == ' ' or i == (ls := len(s) - 1):
            if i == ls:
                buf += v
            if goto_index != 0:
                goto_index = 0
                buf = ''
                continue
            # if all blocks are closed AND first opening char is matching type of last closing char (ie '(' and ')') AND they're both not empty strings OR it's the end of the string
            if (openings == 0 and OPENING_CHARS.find(fst_open) == CLOSING_CHARS.find(lst_close)
                    and OPENING_CHARS.find(fst_open) != -1 and CLOSING_CHARS.find(lst_close) != -1) \
                    and len(fst_open) != 0 and len(lst_close) != 0 \
                    or i == ls:
                #res.append(buf)
                if buf.startswith("{") and buf.endswith("}"):
                    res.append(parse_body(buf))
                elif buf.startswith("(") and buf.endswith(")"):
                    res.append(parse_params(buf))
                elif buf.startswith("[") and buf.endswith("]"):
                    res.append(parse_arr(buf))
                else:
                    res.append(ParseToken(TokenType.ARG, buf))
                fst_open = ''
                lst_close = ''
                openings = 0
            else:
                res.append(ParseToken(TokenType.ARG, buf))
            buf = ''
        elif v == '"':
            token,goto_index = parse_str_literal(s[i:])
            goto_index += i+2
            res.append(token)
        elif v in OPENING_CHARS:
            if fst_open == '':
                fst_open = v
            openings += 1
            buf += v
        elif v in CLOSING_CHARS:
            lst_close = v
            openings -= 1
            buf += v
        elif v != ' ' or openings > 0:
            buf += v
    parse_group_str(res)
    return res