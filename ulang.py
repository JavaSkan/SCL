import string

import TuiErrors
import env
import funlink as fl
import env as ev

LETTERS = string.ascii_letters

OPENING_CHARS = '{[('
CLOSING_CHARS = '}])'

def gethead(args: list):
    try:
        return args[0]
    except IndexError:
        return ""

#TODO update parsing system, with adding generation of tokens (ex:[type:BLOCK,content:['command 1','command2']])

"""
Char positions in a string
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
        return inp.split(c)

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

def parse_body(inp: str) -> list:
    return parse_block(inp,'{','}',';')

def parse_arr(inp):
    return parse_block(inp,'[',']',',')

def parse_params(inp):
    return parse_block(inp,'(',')',',')

"""
I know I know, this is messy and it hurts eyes
but if it works, it works ¯\_(ツ)_/¯
Parses a string knowing there is 'blocks'
blocks/chunks are just delimited areas like {...} or [...] or (...) 
"""
def parse(s:str) -> list:
    buf = ''
    openings = 0
    fst_open = ''
    lst_close = ''
    res = []
    for i,v in enumerate(s):
        if v == ' ' or i == (ls := len(s)-1):
            if i == ls:
                buf += v
            # if all blocks are closed AND first opening char is matching type of last closing char (ie '(' and ')') OR it's the end of the string
            if openings == 0 and OPENING_CHARS.find(fst_open) == CLOSING_CHARS.find(lst_close)\
                             and OPENING_CHARS.find(fst_open)  != -1\
                             and CLOSING_CHARS.find(lst_close) != -1\
                             or i==ls:
                res.append(buf)
                buf = ''
                fst_open = ''
                lst_close = ''
                openings = 0
        if v in OPENING_CHARS:
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
    return res

def is_var_ref(id:str) -> bool:
    return id.startswith(ev._VARREF_SYM) and len(id) > 1

#TODO consider updating var_ref(), make it return the actual value, not as a string, and replacing function calls by 'str(var_ref(...))'
def var_ref(id: str) -> str:
    if is_var_ref(id):
        return str(env.get_value_from_id(id[1:]))
    return id

def is_valid_name(name: str) -> bool:
    return name.isidentifier()

def execute(inst):
    try:
        parsed = parse(inst)
        fl.cmds[gethead(parsed)](parsed[1:])
    except KeyError:
        TuiErrors.TuiError('Unknown Command').trigger()
    except IndexError:
        TuiErrors.TuiError('Args don\'t match').trigger()

def execute_block(block: list):
    for ins in block:
        if type(ins) is str:
            execute(ins)
        elif type(ins) is list:
            execute_block(ins)