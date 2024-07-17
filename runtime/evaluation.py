import re
from parser.keywords import BOOLEAN_KWS
from runtime.allocable import DT_TYPES, Variable
from runtime.errors import SCLError, SCLInvalidBooleanExprError, dangerous
from runtime.env import get_from_id

"""
Boolean Evaluation
"""

@dangerous(note="[EVAL_BOOL_EXPR]")
def eval_bool_expr(blexp: str):
    org = blexp
    blexp = re.sub(BOOLEAN_KWS.AND," and ",blexp)
    blexp = re.sub(BOOLEAN_KWS.OR," or ",blexp)
    blexp = re.sub(BOOLEAN_KWS.NOT," not ",blexp)
    blexp = re.sub(BOOLEAN_KWS.EQL," == ",blexp)
    blexp = re.sub(BOOLEAN_KWS.TRUE," True ",blexp)
    blexp = re.sub(BOOLEAN_KWS.FALSE," False ",blexp)

    while (m := re.search(r"\$\w[\w\d_]*",blexp)) != None:
        var = get_from_id(blexp[m.start() + 1:m.end()])
        if var.type != DT_TYPES.BOOL or type(var) is not Variable:
            return SCLError(f"{var.ident} is not boolean variable")
        blexp = blexp[:m.start()] + str(var.get_value()) + blexp[m.end():]

    try:
        result = eval(blexp)
    except SyntaxError:
        return SCLInvalidBooleanExprError(org)
    else:
        return result