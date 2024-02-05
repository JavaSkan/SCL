import runtime.errors as errors
from runtime import env
import parser.parsing as parsing


def is_var_ref(id:str) -> bool:
    return id.startswith(env._VARREF_SYM) and len(id) > 1


def var_ref(id_: str):
    return env.get_from_id(id_)

def var_ref_str(id_: str) -> str:
    return str(env.get_value_from_id(id_))

def is_valid_name(name: str) -> bool:
    return name.isidentifier()