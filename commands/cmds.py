import os
from parser import parsing as ps, keywords as kws
from runtime import errors
from runtime.errors import dangerous
from runtime import allocable as al
from runtime import env as ev
from runtime import ulang as ul
from runtime import execution as exe
from runtime.execution import SCL_LEXER, SCL_PARSER
from . import operations as oper
from . import manuals


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

def display_f(args: list[ps.Token]):
    for i,arg in enumerate(args):
        printed = arg.value if arg.type != ps.TokenType.VARRF else ul.var_ref_str(arg.value)
        print(printed,end=(" " if i < len(args)-1 else ""))

def displayl_f(args: list[ps.Token]):
    try:
        display_f(args)
        print()
    except IndexError:
        return errors.SCLArgsMismatchError()


def loop_f(args: list[ps.Token]):
    it_tok = ps.try_get(ps.make_value(ps.TokenType.INT,ps.TokenType.BOOL),0,args)
    body_tok = ps.try_get([ps.TokenType.BODY],1,args)
    instructions = body_tok.value
    if (it_int := safe_getv(it_tok, al.DT_TYPES.INT)) != None:
        for i in range(it_int):
            for ins in instructions:
                exe.execute(ins)
    elif safe_getv(it_tok, al.DT_TYPES.BOOL) != None:
        while safe_getv(it_tok, al.DT_TYPES.BOOL):
            for ins in instructions:
                exe.execute(ins)
    else:
        return errors.SCLError("Expected argument of type 'boolean or integer' at position 2")

def new_f(args: list[ps.Token]):
    varkind_tok = ps.try_get([ps.TokenType.ARG],0,args)
    if not varkind_tok.has_specific_value(kws.new_cmd_varkind_kws):
        return errors.SCLError(f"Syntax Error: expected argument with specific value in {kws.new_cmd_varkind_kws}, got {varkind_tok.value}")
    varkind: str = varkind_tok.value

    vartype_tok = ps.try_get([ps.TokenType.ARG],1,args)
    if not vartype_tok.has_specific_value(kws.data_types_keywords):
        return errors.SCLError(f"Syntax Error: expected argument with specific value in {kws.data_types_keywords}, got {varkind_tok.value}")
    vartype: str = vartype_tok.value

    varname_tok = ps.try_get([ps.TokenType.ARG],2,args)
    if not ul.is_valid_name(varname_tok.value):
        return errors.SCLInvalidNameError(varname_tok.value)
    varname: str = varname_tok.value

    value_tok = ps.try_get(ps.make_value(*ps.all_literals()),3,args)
    if (value := safe_getv(value_tok, al.DT_TYPES.str_to_type(vartype))) == None:
        return errors.SCLWrongTypeError(vartype,al.DT_TYPES.guess_type(value_tok.value).__repr__())
    #TODO Fix usage of var_ref_getvalue() in all commands
    #Creation of the variable
    ev.alloc(al.Variable(
         al.VARKIND.str_to_varkind(varkind),
         al.DT_TYPES.str_to_type(vartype),
         varname,
         value)
    )

@errors.dangerous()
def state_f(args):
    nea = ps.no_extra_args(args)
    if nea:
        return nea
    print(f"ALLOCATIONS : {ev._VARS}")
    print(f"ERROR_CODE: {ev._ERR_CODE}")
    print(f"FUNCTION RETURN VALUE : {ev._FUN_RET}")

def end_f(args):
    status_tok = ps.try_get(ps.make_value(ps.TokenType.INT),0,args)
    if (status := safe_getv(status_tok, al.DT_TYPES.INT)) == None:
        return errors.SCLWrongTypeError("int")

    show_tok = ps.try_get(ps.make_value(ps.TokenType.BOOL),1,args)
    if (show := safe_getv(show_tok, al.DT_TYPES.BOOL)) == None:
        return errors.SCLWrongTypeError("bool",al.DT_TYPES.guess_type(show_tok.value).__repr__())

    ev._ERR_CODE = status
    if show:
        print("ended with success" if status == 0 else "ended with failure")
    quit()

def clear_f(args):
    nea = ps.no_extra_args(args)
    if nea:
        return nea
    ev._VARS.clear()

def delete_f(args):
    ident_tok = ps.try_get([ps.TokenType.ARG],0,args)
    var = ul.var_ref(ident_tok.value)
    ev.de_alloc(var)

def set_f(args):
    ident_tok = ps.try_get([ps.TokenType.ARG],0,args)
    if not (var := ul.var_ref(ident_tok.value)):
        return errors.SCLNotFoundError(ident_tok.value)

    new_v_tok = ps.try_get(ps.make_value(*ps.all_literals()),1,args)
    if (new_v := safe_getv(new_v_tok, var.type)) == None:
        return errors.SCLError(f"Expected argument of type '{var.type}' at position ")
    var.set_value(new_v)

def execute_f(args):
    path_tok = ps.try_get(ps.make_value(ps.TokenType.STRLIT),0,args)

    path: str = path_tok.value
    if not os.path.exists(path):
        return errors.SCLNotExistingPathError(path)
    if not os.path.isfile(path):
        return errors.SCLIsNotAFileError(path)
    if not path.endswith('.scl'):
        return errors.SCLWrongExtensionError(path)
    with open(path,'r') as script:
        lines = script.read().split('\n')
        for line in lines:
            exe.execute(line)

def add_f(args):
    modified_tok = ps.try_get([ps.TokenType.ARG],0,args)

    if not (modified_var := ev.get_from_id(modified_tok.value)):
        return errors.SCLNotFoundError(modified_tok.value)
    if not modified_var.type in oper.datatypes_support_add:
        return errors.SCLWrongOperationError("addition",modified_var.type.__repr__())
    modifier_tok = ps.try_get(ps.make_value(*oper.tokentypes_support_add),1,args)

    if (modifier_vl := safe_getv(modifier_tok, modified_var.type)):
        return errors.SCLError(f"Expected argument of type '{modified_var.type}' at position ")
    modified_var.set_value(modified_var.get_value() + modifier_vl)


def sub_f(args):
    modified_tok = ps.try_get([ps.TokenType.ARG], 0, args)

    if not (modified_var := ev.get_from_id(modified_tok.value)):
        return errors.SCLNotFoundError(modified_tok.value)
    if not modified_var.type in oper.datatypes_support_sub:
        return errors.SCLWrongOperationError("subtraction", modified_var.type.__repr__())
    modifier_tok = ps.try_get(ps.make_value(*oper.tokentypes_support_sub), 1, args)

    modifier_vl, er = safe_getv(modifier_tok, modified_var.type)
    if er:
        return er
    modified_var.set_value(modified_var.get_value() - modifier_vl)

def mul_f(args):
    modified_tok = ps.try_get([ps.TokenType.ARG], 0, args)

    if not (modified_var := ev.get_from_id(modified_tok.value)):
        return errors.SCLNotFoundError(modified_tok.value)
    if not modified_var.type in oper.datatypes_support_mul:
        return errors.SCLWrongOperationError("multiplication", modified_var.type.__repr__())
    modifier_tok = ps.try_get(ps.make_value(*oper.tokentypes_support_mul), 1, args)

    modifier_vl, er = safe_getv(modifier_tok, modified_var.type)
    if er:
        return er
    modified_var.set_value(modified_var.get_value() * modifier_vl)

def div_f(args):
    modified_tok = ps.try_get([ps.TokenType.ARG], 0, args)

    if not (modified_var := ev.get_from_id(modified_tok.value)):
        return errors.SCLNotFoundError(modified_tok.value)
    if not modified_var.type in oper.datatypes_support_div:
        return errors.SCLWrongOperationError("division", modified_var.type.__repr__())
    modifier_tok = ps.try_get(ps.make_value(*oper.tokentypes_support_div), 1, args)

    modifier_vl, er = safe_getv(modifier_tok, modified_var.type)
    if er:
        return er
    if modifier_vl == 0:
        return errors.SCLDivisionByZeroError(modified_var.ident)
    if modified_var.type == al.DT_TYPES.INT:
        modified_var.set_value(modified_var.get_value() // modifier_vl)
    else:
        modified_var.set_value(modified_var.get_value() / modifier_vl)

def pow_f(args):
    modified_tok = ps.try_get([ps.TokenType.ARG], 0, args)

    if not (modified_var := ev.get_from_id(modified_tok.value)):
        return errors.SCLNotFoundError(modified_tok.value)
    if not modified_var.type in oper.datatypes_support_pow:
        return errors.SCLWrongOperationError("power", modified_var.type.__repr__())
    modifier_tok = ps.try_get(ps.make_value(*oper.tokentypes_support_pow), 1, args)

    modifier_vl, er = safe_getv(modifier_tok, modified_var.type)
    if er:
        return er
    modified_var.set_value(modified_var.get_value() ** modifier_vl)

def help_f(args):
    cmd_tok = ps.try_get([ps.TokenType.ARG],0,args)

    match cmd_tok.value:
        case 'dp':
            print(manuals.DP)
        case 'dpl':
            print(manuals.DPL)
        case 'loop':
            print(manuals.LOOP)
        case 'new':
            print(manuals.NEW)
        case 'set':
            print(manuals.SET)
        case 'stt':
            print(manuals.STT)
        case 'end':
            print(manuals.END)
        case 'clr':
            print(manuals.CLR)
        case 'del':
            print(manuals.DEL)
        case 'exec':
            print(manuals.EXEC)
        case 'add' | 'sub' | 'mul' | 'div' | 'pow':
            print(manuals.OPERTS)
        case 'help':
            print(manuals.HELP)
        case 'fun':
            print(manuals.FUN)
        case 'ret':
            print(manuals.RET)
        case 'call':
            print(manuals.CALL)
        case 'read':
            print(manuals.READ)
        case 'list':
            print("dp, dpl, loop, new, set, stt, end, clr, del, exec, add, sub, mul, div, pow, help, fun, ret, call, read")
        case _:
            return errors.SCLError("Unknown Command, either it does not exist or there is no manual for it")

def fun_f(args):
    type_tok = ps.try_get([ps.TokenType.ARG],0,args)

    if not type_tok.has_specific_value(kws.data_types_keywords):
        return errors.SCLError(f"Syntax Error: expected argument with specific value in {kws.data_types_keywords}, got {type_tok.value}")
    ftype: al.DT_TYPES = al.DT_TYPES.str_to_type(type_tok.value)
    name_tok = ps.try_get([ps.TokenType.ARG],1,args)

    name :str = name_tok.value
    params_tok = ps.try_get([ps.TokenType.TUPLE], 2, args)

    params = ps.parse_param(params_tok.value)

    body_tok = ps.try_get([ps.TokenType.BODY],3,args)

    body = ps.parse_body(body_tok.value)
    ev.alloc(al.Function(ftype,name,params,body))

def call_f(args):
    name_tok = ps.try_get([ps.TokenType.ARG],0,args)

    if not (fun := ev.get_from_id(name_tok.value)):
        return errors.SCLNotFoundError(name_tok.value)
    if not type(fun) is al.Function:
        return errors.SCLNotCallableError(name_tok.value)
    effective_params_tok = ps.try_get([ps.TokenType.TUPLE], 1, args)

    eff_params: list[str] = ps.parse_param(effective_params_tok.value)
    return fun.execute_fun(eff_params)


def ret_f(args):
    vtok = ps.try_get(ps.make_value(*ps.all_literals()),0,args)

    if vtok.type == ps.TokenType.VARRF:
        if (val := ul.var_ref_str(vtok.value)):
            ev._FUN_RET = val
    else:
        ev._FUN_RET = vtok.value

def read_f(args):
    vartok = ps.try_get([ps.TokenType.ARG],0,args)

    if not (var := ul.var_ref(vartok.value)):
        return errors.SCLNotFoundError(vartok.value)
    usr_input = input()
    if var.type.is_compatible_with_type(usr_input):
        var.set_value(var.type.convert_str_to_value(usr_input))
    else:
        return errors.SCLWrongTypeError(var.type.__repr__())