from parser import parsing as ps
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
def safe_getv(tok: ps.Token, expected_vartype: al.DT_TYPES):
    if tok.type == ps.TokenType.VARRF:
        var = ul.var_ref(tok.value)
        if var.type == expected_vartype:
            return var.get_value()
    else:
        if tok.type == expected_vartype.get_literal_version():
            return expected_vartype.convert_str_to_value(tok.value)
    return None

@dangerous(note="STRICT GETV FUNCTION")
def strict_getv(tok: ps.Token, expected_vartype: al.DT_TYPES):
    if tok.type == ps.TokenType.VARRF:
        var = ul.var_ref(tok.value)
        if var.type == expected_vartype:
            return var.get_value()
        return errors.SCLWrongTypeError(expected_vartype.__repr__(),var.type.__repr__())
    else:
        if tok.type == expected_vartype.get_literal_version():
            return expected_vartype.convert_str_to_value(tok.value)
    return errors.SCLWrongTypeError(expected_vartype.__repr__(),tok.type.__repr__())

def replace_varrf_by_value(values: list):
    for i, v in enumerate(values):
        if type(v) is ps.Token and v.type == ps.TokenType.VARRF:
            values[i] = ul.var_ref(v.value).get_value()