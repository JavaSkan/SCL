from parser import parsing as ps
from parser.tokenizing import Lexer
from parser.parsing import Parser
from runtime.execution import Executor
from parser.tokens import Token, TokenType
from runtime import allocable as al
from runtime import ulang as ul
from runtime import errors
from runtime.errors import dangerous

"""
Gets a token which is either a VARRF token or a literal
and an expected datatype

If the token is a variable reference then it checks if the expected datatype is matching and it returns the value of that variable
if it is existing

If the token is a literal, then it check if it's matching with the expected datatype
and returns the corresponding value
"""
def safe_getv(tok: Token, expected_vartype: al.DT_TYPES,isarray=False):
    if tok.type == TokenType.VARRF:
        var = ul.var_ref(tok.value)
        if var.type == expected_vartype:
            if isarray:
                if type(var) is not al.Array:
                    return None
            return var.get_value()
    else:
        if tok.type == expected_vartype.get_literal_version():
            return expected_vartype.convert_str_to_value(tok.value)
    return None

@dangerous(note="VARIABLE REFERENCING ISSUE")
def strict_getv(tok: Token, expected_vartype: al.DT_TYPES, isarray=False):
    if tok.type == TokenType.VARRF:
        var = ul.var_ref(tok.value)
        if var.type == expected_vartype or expected_vartype == al.DT_TYPES.ANY:
            if isarray:
                if type(var) is not al.Array:
                    return errors.SCLWrongTypeError(al.Array.__name__,var.type.name)
            return var.get_value()
        return errors.SCLWrongTypeError(expected_vartype.name,var.type.name)
    else:
        if isarray:
            if tok.type == TokenType.ARR:
                return ps.eval_array_values(tok)
            else:
                return errors.SCLWrongTypeError(TokenType.ARR.__repr__(),tok.type.name)
        if tok.type == expected_vartype.get_literal_version():
            return expected_vartype.convert_str_to_value(tok.value)
    return errors.SCLWrongTypeError(expected_vartype.name,tok.type.name)

def replace_varrf_by_value(values: list):
    for i, v in enumerate(values):
        if type(v) is Token and v.type == TokenType.VARRF:
            values[i] = ul.var_ref(v.value).get_value()

def make_value(*token_types):
    return [TokenType.VARRF] + [t for t in token_types]