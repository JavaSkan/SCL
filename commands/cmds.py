import os
from parser import parsing as ps, keywords as kws
from runtime import errors
from runtime import allocable as al
from runtime import env as ev
from runtime import ulang as ul
from runtime import execution as exe
from . import operations as oper
from . import manuals


"""
Gets a token which is either a varref token or another type
and an expected datatype

If the token is a variable reference then it checks if the expected datatype is matching and it returns the value of that variable
if it is existing

If the token is a type literal, then it check if it's matching with the expected datatype
and returns the corresponding value

The function always return a tuple with the value put in first position and the error in the second one
one or both can be None
(<value>,<error>)
"""
def var_ref_getvalue(tok: ps.ParseToken, expected_vartype: al.DT_TYPES):
    if tok.type == ps.TokenType.VARREF:
        if not (var := ul.var_ref(tok.value)):
            return (None, errors.SCLNotFoundError(tok.value))
        elif var.type == expected_vartype:
            return var.get_value(),None
        else:
            return None,errors.SCLWrongTypeError(expected_vartype.__repr__(), var.type.__repr__())
    else:
        match tok.type:
            case ps.TokenType.INTLIT:
                if expected_vartype == al.DT_TYPES.INT:
                    return int(tok.value),None
                else:
                    return None,errors.SCLWrongTypeError(expected_vartype.__repr__(), ps.TokenType.INTLIT.__repr__())
            case ps.TokenType.FLTLIT:
                if expected_vartype == al.DT_TYPES.FLT:
                    return float(tok.value),None
                else:
                    return None, errors.SCLWrongTypeError(expected_vartype.__repr__(), ps.TokenType.FLTLIT.__repr__())
            case ps.TokenType.STRLIT:
                if expected_vartype == al.DT_TYPES.STR:
                    return tok.value,None
                else:
                    return None,errors.SCLWrongTypeError(expected_vartype.__repr__(), ps.TokenType.STRLIT.__repr__())
            case ps.TokenType.BOOLLIT:
                if expected_vartype == al.DT_TYPES.BOOL:
                    return tok.value == 'true',None
                else:
                    return None,errors.SCLWrongTypeError(expected_vartype.__repr__(), ps.TokenType.BOOLLIT.__repr__())
            case _:
                return None,errors.SCLError("Invalid token, is not compatible with datatypes")



def display_f(args: list[ps.ParseToken]):
    for i,arg in enumerate(args):
        printed = arg.value if arg.type != ps.TokenType.VARREF else ul.var_ref_str(arg.value)
        print(printed,end=(" " if i < len(args)-1 else ""))

def displayl_f(args: list[ps.ParseToken]):
    try:
        display_f(args)
        print()
    except IndexError:
        return  errors.SCLArgsMismatchError()


def loop_f(args: list[ps.ParseToken]):
    it_tok, er = ps.try_get(ps.TokenType.make_value(ps.TokenType.INTLIT,ps.TokenType.BOOLLIT),0,args)
    if er:
        return er
    it_int, er_intlit = var_ref_getvalue(it_tok,al.DT_TYPES.INT)
    it_bool, er_boollit = var_ref_getvalue(it_tok,al.DT_TYPES.BOOL)
    if er_intlit and er_boollit:
        return errors.SCLError("Expected either a boolean or an integer at position 2")
    body_tok, ers = ps.try_get([ps.TokenType.BODY],1,args)
    if ers:
        return ers
    instructions = ps.parse_body(body_tok.value)
    if not er_intlit:
        for i in range(it_int):
            for ins in instructions:
                exe.execute(ins)
    else:
        while var_ref_getvalue(it_tok,al.DT_TYPES.BOOL)[0]:
            for ins in instructions:
                exe.execute(ins)


def new_f(args: list[ps.ParseToken]):
    varkind_tok, er = ps.try_get([ps.TokenType.ARG],0,args)
    if er:
        return er
    if not varkind_tok.has_specific_value(kws.new_cmd_varkind_kws):
        return errors.SCLError(f"Syntax Error: expected argument with specific value in {kws.new_cmd_varkind_kws}, got {varkind_tok.value}")
    varkind: str = varkind_tok.value

    vartype_tok, er = ps.try_get([ps.TokenType.ARG],1,args)
    if er:
        return er
    if not vartype_tok.has_specific_value(kws.data_types_keywords):
        return errors.SCLError(f"Syntax Error: expected argument with specific value in {kws.data_types_keywords}, got {varkind_tok.value}")
    vartype: str = vartype_tok.value

    varname_tok,er = ps.try_get([ps.TokenType.ARG],2,args)
    if er:
        return er
    if not ul.is_valid_name(varname_tok.value):
        return errors.SCLInvalidNameError(varname_tok.value)
    varname: str = varname_tok.value

    value_tok, er = ps.try_get(ps.TokenType.make_value(*ps.all_literals()),3,args)
    if er:
        return er
    value, getvalueerr = var_ref_getvalue(value_tok,al.DT_TYPES.str_to_type(vartype))
    if getvalueerr:
        return getvalueerr

    #Creation of the variable
    ev.alloc(al.Variable(
         al.VARKIND.str_to_varkind(varkind),
         al.DT_TYPES.str_to_type(vartype),
         varname,
         value)
    )


def state_f(args):
    nea = ps.no_extra_args(args)
    if nea:
        return nea
    print(f"ALLOCATIONS : {ev._VARS}")
    print(f"ERROR_CODE: {ev._ERR_CODE}")
    print(f"FUNCTION RETURN VALUE : {ev._FUN_RET}")

def end_f(args):
    status_tok, er = ps.try_get(ps.TokenType.make_value(ps.TokenType.INTLIT),0,args)
    if er:
        return er
    status,er = var_ref_getvalue(status_tok,al.DT_TYPES.INT)
    if er:
        return er
    show_tok, er = ps.try_get(ps.TokenType.make_value(ps.TokenType.BOOLLIT),1,args)
    if er:
        return er
    show,er = var_ref_getvalue(show_tok,al.DT_TYPES.BOOL)
    if er:
        return er
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
    ident_tok, er = ps.try_get([ps.TokenType.ARG],0,args)
    if er:
        return er
    if not (var := ul.var_ref(ident_tok.value)):
        return errors.SCLNotFoundError(ident_tok.value)
    ev.de_alloc(var)


def set_f(args):
    ident_tok, er = ps.try_get([ps.TokenType.ARG],0,args)
    if er:
        return er
    if not (var := ul.var_ref(ident_tok.value)):
        return errors.SCLNotFoundError(ident_tok.value)
    new_v_tok, er = ps.try_get(ps.TokenType.make_value(*ps.all_literals()),1,args)
    if er:
        return er
    new_v, er = var_ref_getvalue(new_v_tok,var.type)
    if er:
        return er
    var.set_value(new_v)

def execute_f(args):
    path_tok, er = ps.try_get(ps.TokenType.make_value(ps.TokenType.STRLIT),0,args)
    if er:
        return er
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
    modified_tok, er = ps.try_get([ps.TokenType.ARG],0,args)
    if er:
        return er
    if not (modified_var := ev.get_from_id(modified_tok.value)):
        return errors.SCLNotFoundError(modified_tok.value)
    if not modified_var.type in oper.datatypes_support_add:
        return errors.SCLWrongOperationError("addition",modified_var.type.__repr__())
    modifier_tok, er = ps.try_get(ps.TokenType.make_value(*oper.tokentypes_support_add),1,args)
    if er:
        return er
    modifier_vl, er = var_ref_getvalue(modifier_tok,modified_var.type)
    if er:
        return er
    modified_var.set_value(modified_var.get_value() + modifier_vl)


def sub_f(args):
    modified_tok, er = ps.try_get([ps.TokenType.ARG], 0, args)
    if er:
        return er
    if not (modified_var := ev.get_from_id(modified_tok.value)):
        return errors.SCLNotFoundError(modified_tok.value)
    if not modified_var.type in oper.datatypes_support_sub:
        return errors.SCLWrongOperationError("subtraction", modified_var.type.__repr__())
    modifier_tok, er = ps.try_get(ps.TokenType.make_value(*oper.tokentypes_support_sub), 1, args)
    if er:
        return er
    modifier_vl, er = var_ref_getvalue(modifier_tok, modified_var.type)
    if er:
        return er
    modified_var.set_value(modified_var.get_value() - modifier_vl)

def mul_f(args):
    modified_tok, er = ps.try_get([ps.TokenType.ARG], 0, args)
    if er:
        return er
    if not (modified_var := ev.get_from_id(modified_tok.value)):
        return errors.SCLNotFoundError(modified_tok.value)
    if not modified_var.type in oper.datatypes_support_mul:
        return errors.SCLWrongOperationError("multiplication", modified_var.type.__repr__())
    modifier_tok, er = ps.try_get(ps.TokenType.make_value(*oper.tokentypes_support_mul), 1, args)
    if er:
        return er
    modifier_vl, er = var_ref_getvalue(modifier_tok, modified_var.type)
    if er:
        return er
    modified_var.set_value(modified_var.get_value() * modifier_vl)

def div_f(args):
    modified_tok, er = ps.try_get([ps.TokenType.ARG], 0, args)
    if er:
        return er
    if not (modified_var := ev.get_from_id(modified_tok.value)):
        return errors.SCLNotFoundError(modified_tok.value)
    if not modified_var.type in oper.datatypes_support_div:
        return errors.SCLWrongOperationError("division", modified_var.type.__repr__())
    modifier_tok, er = ps.try_get(ps.TokenType.make_value(*oper.tokentypes_support_div), 1, args)
    if er:
        return er
    modifier_vl, er = var_ref_getvalue(modifier_tok, modified_var.type)
    if er:
        return er
    if modifier_vl == 0:
        return errors.SCLDivisionByZeroError(modified_var.ident)
    if modified_var.type == al.DT_TYPES.INT:
        modified_var.set_value(modified_var.get_value() // modifier_vl)
    else:
        modified_var.set_value(modified_var.get_value() / modifier_vl)

def pow_f(args):
    modified_tok, er = ps.try_get([ps.TokenType.ARG], 0, args)
    if er:
        return er
    if not (modified_var := ev.get_from_id(modified_tok.value)):
        return errors.SCLNotFoundError(modified_tok.value)
    if not modified_var.type in oper.datatypes_support_pow:
        return errors.SCLWrongOperationError("power", modified_var.type.__repr__())
    modifier_tok, er = ps.try_get(ps.TokenType.make_value(*oper.tokentypes_support_pow), 1, args)
    if er:
        return er
    modifier_vl, er = var_ref_getvalue(modifier_tok, modified_var.type)
    if er:
        return er
    modified_var.set_value(modified_var.get_value() ** modifier_vl)

def help_f(args):
    cmd_tok, er = ps.try_get([ps.TokenType.ARG],0,args)
    if er:
        return er
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
    type_tok, err = ps.try_get([ps.TokenType.ARG],0,args)
    if err:
        return err
    if not type_tok.has_specific_value(kws.data_types_keywords):
        return errors.SCLError(f"Syntax Error: expected argument with specific value in {kws.data_types_keywords}, got {type_tok.value}")
    ftype: al.DT_TYPES = al.DT_TYPES.str_to_type(type_tok.value)
    name_tok, err = ps.try_get([ps.TokenType.ARG],1,args)
    if err:
        return name_tok
    name :str = name_tok.value
    params_tok, err = ps.try_get([ps.TokenType.PARAM],2,args)
    if err:
        return err
    params = ps.parse_param(params_tok.value)
    if err:
        return err
    body_tok, err = ps.try_get([ps.TokenType.BODY],3,args)
    if err:
        return err
    body = ps.parse_body(body_tok.value)
    ev.alloc(al.Function(ftype,name,params,body))

def call_f(args):
    name_tok, err = ps.try_get([ps.TokenType.ARG],0,args)
    if err:
        return err
    if not (fun := ev.get_from_id(name_tok.value)):
        return errors.SCLNotFoundError(name_tok.value)
    if not type(fun) is al.Function:
        return errors.SCLNotCallableError(name_tok.value)
    effective_params_tok, err = ps.try_get([ps.TokenType.PARAM],1,args)
    if err:
        return err
    eff_params: list[str] = ps.parse_param(effective_params_tok.value)
    return fun.execute_fun(eff_params)


def ret_f(args):
    vtok, err = ps.try_get(ps.TokenType.make_value(*ps.all_literals()),0,args)
    if err:
        return err
    if vtok.type == ps.TokenType.VARREF:
        if (val := ul.var_ref_str(vtok.value)):
            ev._FUN_RET = val
    else:
        ev._FUN_RET = vtok.value

def read_f(args):
    vartok, err = ps.try_get([ps.TokenType.ARG],0,args)
    if err:
        return err
    if not (var := ul.var_ref(vartok.value)):
        return errors.SCLNotFoundError(vartok.value)
    usr_input = input()
    if var.is_compatible_with_type(usr_input):
        var.set_value(var.convert_str_value_to_type(usr_input))
    else:
        return errors.SCLWrongTypeError(var.type.__repr__())