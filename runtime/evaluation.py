import re
from parser.keywords import BOOLEAN_KWS
from runtime.errors import SCLInvalidBooleanExprError, dangerous
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
        blexp = blexp[:m.start()] + var.get_insertion_value() + blexp[m.end():]

    try:
        result = eval(blexp)
    except Exception as e:
        return SCLInvalidBooleanExprError(org,py_ind=e.__class__.__name__)
    else:
        return result