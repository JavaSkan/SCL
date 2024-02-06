import os
from parser import parsing as ps, keywords as kws
from runtime import errors
from runtime import allocable as al
from runtime import env as ev
from runtime import ulang as ul
from runtime import execution as exe
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
    it_tok, er = ps.try_get(ps.TokenType.make_value(ps.TokenType.INTLIT),0,args)
    if er:
        return er
    it, er = var_ref_getvalue(it_tok,al.DT_TYPES.INT)
    if er:
        return er
    body_tok, ers = ps.try_get([ps.TokenType.BODY],1,args)
    if er:
        return er
    instructions = ps.parse_body(body_tok.value)
    for i in range(it):
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
        return errors.SCLError(f"Syntax Error: expected argument with specific value in {kws.new_cmd_varkind_kws}, got {varkind_tok.value}")
    vartype: str = vartype_tok.value

    varname_tok,er = ps.try_get([ps.TokenType.ARG],2,args)
    if er:
        return er
    if not ul.is_valid_name(varname_tok.value):
        return errors.SCLInvalidNameError(varname_tok.value)
    varname: str = varname_tok.value

    value_tok, er = ps.try_get(ps.TokenType.make_value(ps.TokenType.INTLIT,ps.TokenType.FLTLIT,ps.TokenType.STRLIT,ps.TokenType.BOOLLIT),3,args)
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
    print(f"VARIABLE REFERENCING SYMBOL : {ev._VARREF_SYM}")

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
    if (var := ev.get_from_id(args[0])) == None:
        errors.SCLNotFoundError(args[0]).trigger()
    new = ev.get_from_id(args[1][1:]) if ul.is_var_ref(args[1]) else args[1]
    if type(new) is str:
        if var.is_compatible_with_type(new):
            var.set_value(var.convert_str_value_to_type(new))
        else:
            errors.SCLWrongTypeError(var.type.__repr__()).trigger()
    else:
        if var.type == new.type:
            var.set_value(new.get_value())
        else:
            errors.SCLWrongTypeError(var.type.__repr__(),new.type.__repr__()).trigger()

def execute_f(args):
    if os.path.exists(args[0]):
        if args[0].endswith(".scl"):
            with open(args[0],"r") as f:
                lines = f.read().split("\n")
                for line in lines:
                    exe.execute(line)
        else:
            errors.SCLError("Incorrect file extension").trigger()
    else:
        errors.SCLError("There is not such file").trigger()

def add_f(args):
    if (var1 := ev.get_from_id(args[0])) == None:
        errors.SCLNotFoundError(args[0]).trigger()
    var2 = ev.get_from_id(args[1][1:]) if ul.is_var_ref(args[1]) else args[1]
    if type(var1) is al.Array:
        var1.add_v(var2)
        return
    if type(var2) is str:
        if var1.is_compatible_with_type(var2):
            var1.set_value(var1.get_value() + var1.convert_str_value_to_type(var2))
        else:
            errors.SCLWrongTypeError(var1.type.__repr__()).trigger()
    else:
        if var2 == None:
            errors.SCLNotFoundError(args[1]).trigger()
        if var1.is_compatible_with_type(str(var2.get_value())):
            var1.set_value(var1.get_value() + var2.get_value())
        else:
            errors.SCLWrongTypeError(var1.type.__repr__(),var2.type.__repr__()).trigger()


def sub_f(args):
    if (var1 := ev.get_from_id(args[0])) == None:
        errors.SCLNotFoundError(args[0]).trigger()
    var2 = ev.get_from_id(args[1][1:]) if ul.is_var_ref(args[1]) else args[1]
    if type(var1) is al.Array:
        errors.SCLWrongOperationError("subtraction","array")
        return
    if type(var2) is str:
        if var1.is_compatible_with_type(var2):
            if var1.type in (al.DT_TYPES.INT,al.DT_TYPES.FLT):
                var1.set_value(var1.get_value() - var1.convert_str_value_to_type(var2))
            else:
                errors.SCLWrongOperationError("subtraction",var1.type.__repr__()).trigger()
        else:
            errors.SCLWrongTypeError(var1.type.__repr__()).trigger()
    else:
        if var2 == None:
            errors.SCLNotFoundError(args[1]).trigger()
        if var1.is_compatible_with_type(str(var2.get_value())):
            if var1.type in (al.DT_TYPES.INT, al.DT_TYPES.FLT):
                var1.set_value(var1.get_value() - var2.get_value())
            else:
                errors.SCLWrongOperationError("subtraction", var1.type.__repr__()).trigger()
        else:
            errors.SCLWrongTypeError(var1.type.__repr__(),var2.type.__repr__()).trigger()

def mul_f(args):
    if (var1 := ev.get_from_id(args[0])) == None:
        errors.SCLNotFoundError(args[0]).trigger()
    var2 = ev.get_from_id(args[1][1:]) if ul.is_var_ref(args[1]) else args[1]
    if type(var1) is al.Array:
        errors.SCLWrongOperationError("multiplication", "array")
        return
    if type(var2) is str:
        if var1.is_compatible_with_type(var2):
            if var1.type in (al.DT_TYPES.INT, al.DT_TYPES.FLT):
                var1.set_value(var1.get_value() * var1.convert_str_value_to_type(var2))
            else:
                errors.SCLWrongOperationError("multiplication", var1.type.__repr__()).trigger()
        else:
            errors.SCLWrongTypeError(var1.type.__repr__()).trigger()
    else:
        if var2 == None:
            errors.SCLNotFoundError(args[1]).trigger()
        if var1.is_compatible_with_type(str(var2.get_value())):
            if var1.type in (al.DT_TYPES.INT, al.DT_TYPES.FLT):
                var1.set_value(var1.get_value() * var2.get_value())
            else:
                errors.SCLWrongOperationError("multiplication", var1.type.__repr__()).trigger()
        else:
            errors.SCLWrongTypeError(var1.type.__repr__(), var2.type.__repr__()).trigger()

def div_f(args):
    if (var1 := ev.get_from_id(args[0])) == None:
        errors.SCLNotFoundError(args[0]).trigger()
    var2 = ev.get_from_id(args[1][1:]) if ul.is_var_ref(args[1]) else args[1]
    if type(var1) is al.Array:
        errors.SCLWrongOperationError("division", "array")
        return
    if type(var2) is str:
        if var1.is_compatible_with_type(var2):
            if float(var2) == 0.0:
                errors.SCLDivisionByZeroError(var1.id).trigger()
            if var1.type == al.DT_TYPES.INT:
                var1.set_value(var1.get_value() // var1.convert_str_value_to_type(var2))
            elif var1.type == al.DT_TYPES.FLT:
                var1.set_value(var1.get_value() / var1.convert_str_value_to_type(var2))
            else:
                errors.SCLWrongOperationError("division", var1.type.__repr__()).trigger()
        else:
            errors.SCLWrongTypeError(var1.type.__repr__()).trigger()
    else:
        if var2 == None:
            errors.SCLNotFoundError(args[1]).trigger()
        if var1.is_compatible_with_type(str(var2.get_value())):
            if var2.get_value() == 0.0:
                errors.SCLDivisionByZeroError(var1.id).trigger()
            if var1.type == al.DT_TYPES.INT:
                var1.set_value(var1.get_value() // var2.get_value())
            elif var1.type == al.DT_TYPES.FLT:
                var1.set_value(var1.get_value() / var2.get_value())
            else:
                errors.SCLWrongOperationError("division", var1.type.__repr__()).trigger()
        else:
            errors.SCLWrongTypeError(var1.type.__repr__(), var2.type.__repr__()).trigger()

def pow_f(args):
    if (var1 := ev.get_from_id(args[0])) == None:
        errors.SCLNotFoundError(args[0]).trigger()
    var2 = ev.get_from_id(args[1][1:]) if ul.is_var_ref(args[1]) else args[1]
    if type(var1) is al.Array:
        errors.SCLWrongOperationError("power", "array")
        return
    if type(var2) is str:
        if var1.is_compatible_with_type(var2):
            if var1.type in (al.DT_TYPES.INT, al.DT_TYPES.FLT):
                var1.set_value(var1.get_value() ** var1.convert_str_value_to_type(var2))
            else:
                errors.SCLWrongOperationError("power", var1.type.__repr__()).trigger()
        else:
            errors.SCLWrongTypeError(var1.type.__repr__()).trigger()
    else:
        if var2 == None:
            errors.SCLNotFoundError(args[1]).trigger()
        if var1.is_compatible_with_type(str(var2.get_value())):
            if var1.type in (al.DT_TYPES.INT, al.DT_TYPES.FLT):
                var1.set_value(var1.get_value() ** var2.get_value())
            else:
                errors.SCLWrongOperationError("power", var1.type.__repr__()).trigger()
        else:
            errors.SCLWrongTypeError(var1.type.__repr__(), var2.type.__repr__()).trigger()

def help_f(args):
    match args[0]:
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
        case 'vr':
            print(manuals.VR)
        case 'call':
            print(manuals.CALL)
        case 'read':
            print(manuals.READ)
        case 'list':
            print("dp, dpl, loop, new, set, stt, end, clr, del, exec, add, sub, mu, div, pow, help, fun, ret, vr, call, enable_eq, disable_eq, read")
        case _:
            errors.SCLError("Unknown Command, either it does not exist or there is no manual for it").trigger()

def fun_f(args):
    if not ul.is_valid_name(args[0]):
        errors.SCLInvalidNameError(args[0]).trigger()

    #fun <name> {body}
    if (alen := len(args)) == 2:
        al.Function(args[0],None,ul.parse_body(args[1]))
    #fun <name> (params) {body}
    elif alen == 3:
        al.Function(args[0],ul.parse_params(args[1]),ul.parse_body(args[2]))

def ret_f(args):
    ev._FUN_RET = ul.var_ref_str(args[0])

def vr_f(args):
    if args[0] == 'set':
        ev._VARREF_SYM = args[1]
    elif args[0] == 'reset':
        ev._VARREF_SYM = '$'
    else:
        errors.SCLError(f'{args[0]} is not a valid argument for this command').trigger()

def call_f(args):
    if (fun := ev.get_from_id(args[0])) == None:
        errors.SCLNotFoundError(args[0]).trigger()
    if type(fun) is not al.Function:
        errors.SCLNotCallableError(args[0]).trigger()
    fun.execute_fun(args[1:])

def read_f(args):
    if (var := ev.get_from_id(args[0])) == None:
        errors.SCLNotFoundError(args[0]).trigger()
    user_input = input("")
    if var.is_compatible_with_type(user_input):
        var.set_value(var.convert_str_value_to_type(user_input))
    else:
        errors.SCLWrongTypeError(var.type.__repr__()).trigger()
