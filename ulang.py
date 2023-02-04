import string

import env
import funlink as fl
import env as ev

LETTERS = string.ascii_letters

#char positions in string
def cpos(inp: str, c) -> list:
    poss = []
    for i in range(len(inp)):
        if inp[i] == c:
            poss.append(i)
    return poss

def gethead(args: list):
    try:
        return args[0]
    except IndexError:
        return ""

def parse_binp(inp: str, c) -> list:
    res = []
    sc_pos = cpos(inp, c)
    lpos = cpos(inp, '{')
    rpos = cpos(inp, '}')
    #if there is no { or } then it returns the whole split string
    if len(lpos) == len(rpos) == 0:
        return inp.split(c)
    prev_sc_pos = 0

    for i in range(len(sc_pos)):
        #checks if the ; is not included in a block, or array
        if sc_pos[i] < lpos[0] or sc_pos[i] > rpos[len(rpos)-1]:
            res.append(inp[prev_sc_pos:sc_pos[i]])
            prev_sc_pos = sc_pos[i]+1
    res.append(inp[prev_sc_pos:len(inp)])
    return res

def parse(line: str) -> list:
    return parse_binp(line,' ')

def parse_block(inp: str) -> list:
    lpos = cpos(inp,'{')
    rpos = cpos(inp,'}')

    if len(lpos) > len(rpos):
        print(f"Missing {'}'} after the last one at position {rpos[len(rpos)-1]}")
        return []
    elif len(lpos) < len(rpos):
        print(f"Missing {'{'} before the first one at position {lpos[0]}")
        return []
    elif len(lpos) == len(rpos) == 0:
        return parse(inp)

    res = parse_binp(inp[lpos[0]+1:rpos[len(rpos)-1]],';')

    for i in range(len(res)):
        if res[i].startswith(' '):
            res[i] = res[i][1:]
        if res[i].endswith(' '):
            res[i] = res[i][:-1]
        if res[i].startswith('{') and res[i].endswith('}'):
            res[i] = parse_block(res[i])
    return res

def parse_instance(line: str) -> list:
    return parse_binp(line, ';')

def parse_arr(inp):
    lpos = cpos(inp, '[')
    rpos = cpos(inp, ']')

    if len(lpos) > len(rpos):
        print(f"Missing {']'} after the last one at position {rpos[len(rpos) - 1]}")
        return []
    elif len(lpos) < len(rpos):
        print(f"Missing {'['} before the first one at position {lpos[0]}")
        return []
    elif len(lpos) == len(rpos) == 0:
        return parse(inp)

    res = parse_binp(inp[lpos[0] + 1:rpos[len(rpos) - 1]], ',')

    for i in range(len(res)):
        if res[i].startswith(' '):
            res[i] = res[i][1:]
        if res[i].endswith(' '):
            res[i] = res[i][:-1]
        if res[i].startswith('[') and res[i].endswith(']'):
            res[i] = parse_block(res[i])
    return res

def var_ref(id: str) -> str:
    if id.startswith(ev._VARREF_SYM):
        if len(id) > 1:
            return str(env.get_value_from_id(id[1:]))
    return id

def is_valid_name(name: str) -> bool:
    for c in name:
        if c not in LETTERS:
            return False
    return True

def rem_endline(inp: str) -> str:
    out = ""
    for c in str:
        if c != '\n':
            out += c
    return out

def execute(inst):
    try:
        parsed = parse(inst)
        fl.cmds[gethead(parsed)](parsed)
    except KeyError:
        print('Unknown Command')
    except IndexError:
        print('Args don\'t match')

def execute_block(block: list):
    for ins in block:
        if type(ins) is str:
            execute(ins)
        elif type(ins) is list:
            execute_block(ins)