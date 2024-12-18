import os

import commands
import parser.tokens
from parser import keywords as kws
from runtime import env as ev
from runtime import execution as exe
from runtime.allocable import DT_TYPES
from runtime.env import Environment
from runtime.errors import SCLWrongTypeError
from runtime.evaluation import eval_bool_expr
from . import operations as oper
from . import manuals

from . import *

def display_f(args: list[Token]):
    for i,arg in enumerate(args):
        printed = arg.value if arg.type != TokenType.VARRF else ul.var_ref_str(arg.value)
        print(printed,end="")

def displayl_f(args: list[Token]):
    try:
        display_f(args)
        print()
    except IndexError:
        return errors.SCLArgsMismatchError()


def loop_f(args: list[Token]):
    it_tok = ps.try_get(commands.make_value(TokenType.INT, TokenType.BOOL, TokenType.BLEXP), 0, args)
    body_tok = ps.try_get([TokenType.BODY],1,args)
    instructions = body_tok.value
    loop_exe = Executor()
    if (it_int := safe_getv(it_tok, al.DT_TYPES.INT)) != None:
        for i in range(it_int):
            for ins in instructions:
                loop_exe.execute(ins)
    elif safe_getv(it_tok, al.DT_TYPES.BOOL) != None:
        while safe_getv(it_tok, al.DT_TYPES.BOOL):
            for ins in instructions:
                loop_exe.execute(ins)
    elif it_tok.type == TokenType.BLEXP:
        while eval_bool_expr(it_tok.value):
            for ins in instructions:
                loop_exe.execute(ins)
    else:
        return errors.SCLError("Expected argument of type 'boolean or integer' at position 2")

def new_f(args: list[Token]):
    varkind_tok = ps.try_get([TokenType.IDT], 0, args)
    if not varkind_tok.has_specific_value(kws.varkinds):
        return errors.SCLError(f"Syntax Error: expected argument with specific value in {kws.varkinds}, got {varkind_tok.value}")
    varkind: str = varkind_tok.value

    vartype_tok = ps.try_get([TokenType.IDT], 1, args)
    if not vartype_tok.has_specific_value(kws.basic_datatypes):
        return errors.SCLError(f"Syntax Error: expected argument with specific value in {kws.basic_datatypes}, got {varkind_tok.value}")
    vartype: str = vartype_tok.value

    varname_tok = ps.try_get([TokenType.IDT], 2, args)
    if not ul.is_valid_name(varname_tok.value):
        return errors.SCLInvalidIdentError(varname_tok.value)
    varname: str = varname_tok.value

    value_tok = ps.try_get(commands.make_value(*parser.tokens.all_literals()), 3, args)
    if (value := safe_getv(value_tok, al.DT_TYPES.str_to_type(vartype))) == None:
        return errors.SCLWrongTypeError(vartype,al.DT_TYPES.guess_type(value_tok.value).name)

    #Creation of the variable
    ev.alloc(al.Variable(
         al.VARKIND.str_to_varkind(varkind),
         al.DT_TYPES.str_to_type(vartype),
         varname,
         value)
    )

@errors.dangerous()
def state_f(args: list[Token]):
    nea = ps.no_extra_args(args)
    if nea:
        return nea
    print(f"ALLOCATIONS : {ev.CURENV.allocations}")
    print(f"ALIASES: {ev.CURENV.aliases}")
    print(f"ERROR_CODE: {ev.CURENV.exit_code}")
    print(f"FUNCTION RETURN VALUE: {ev.CURENV.fun_ret}")

def end_f(args: list[Token]):
    status_tok = ps.try_get(commands.make_value(TokenType.INT), 0, args)
    if (status := safe_getv(status_tok, al.DT_TYPES.INT)) == None:
        return errors.SCLWrongTypeError("int")

    show_tok = ps.try_get(commands.make_value(TokenType.BOOL), 1, args)
    if (show := safe_getv(show_tok, al.DT_TYPES.BOOL)) == None:
        return errors.SCLWrongTypeError("bool",al.DT_TYPES.guess_type(show_tok.value).name)

    ev.CURENV.exit_code = status
    if show:
        print("ended with success" if status == 0 else "ended with failure" if status == 1 else f"ended with exit code {status}")
    os._exit(ev.CURENV.exit_code)

def clear_f(args: list[Token]):
    nea = ps.no_extra_args(args)
    if nea:
        return nea
    ev.CURENV.allocations.clear()

def delete_f(args: list[Token]):
    ident_tok = ps.try_get([TokenType.IDT], 0, args)
    var = ul.var_ref(ident_tok.value)
    ev.de_alloc(var)

def set_f(args: list[Token]):
    ident_tok = ps.try_get([TokenType.IDT], 0, args)
    if not (var := ul.var_ref(ident_tok.value)):
        return errors.SCLNotFoundError(ident_tok.value)

    new_v_tok = ps.try_get(commands.make_value(*parser.tokens.all_literals()), 1, args)
    if (new_v := safe_getv(new_v_tok, var.type)) == None:
        return errors.SCLError(f"Expected argument of type '{var.type.name}' at position 3")
    var.set_value(new_v)

def execute_f(args: list[Token]):
    path_tok = ps.try_get(commands.make_value(TokenType.STR), 0, args)
    path = strict_getv(path_tok,DT_TYPES.STR)
    if not os.path.exists(path):
        return errors.SCLNotExistingPathError(path)
    if not os.path.isfile(path):
        return errors.SCLIsNotAFileError(path)
    if not path.endswith('.scl'):
        return errors.SCLWrongExtensionError(path)
    cross_env_tok = ps.try_get(commands.make_value(TokenType.BOOL), 1, args)
    if (cross_env := safe_getv(cross_env_tok,DT_TYPES.BOOL)) == None:
        return SCLWrongTypeError(DT_TYPES.BOOL.name)
    with open(path,'r',encoding="utf-8-sig") as script:
        used_env = ev.CURENV if cross_env else Environment()
        with Executor(environment=used_env) as file_executor:
            file_executor.load_script(script.read())
            parsed_content = file_executor.parser.parse_lines()
            for set_of_tokens in parsed_content:
                file_executor.execute_parsed(set_of_tokens)

def add_f(args: list[Token]):
    modified_tok = ps.try_get([TokenType.IDT], 0, args)

    if not (modified_var := ev.get_from_id(modified_tok.value)):
        return errors.SCLNotFoundError(modified_tok.value)
    if not modified_var.type in oper.datatypes_support_add:
        return errors.SCLWrongOperationError("addition",modified_var.type.name)
    modifier_tok = ps.try_get(commands.make_value(*oper.tokentypes_support_add), 1, args)

    if (modifier_vl := safe_getv(modifier_tok, modified_var.type)) == None:
        return errors.SCLError(f"Expected argument of type '{modified_var.type.name}' at position 3")
    modified_var.set_value(modified_var.get_value() + modifier_vl)


def sub_f(args: list[Token]):
    modified_tok = ps.try_get([TokenType.IDT], 0, args)

    if not (modified_var := ev.get_from_id(modified_tok.value)):
        return errors.SCLNotFoundError(modified_tok.value)
    if not modified_var.type in oper.datatypes_support_sub:
        return errors.SCLWrongOperationError("subtraction", modified_var.type.name)
    modifier_tok = ps.try_get(commands.make_value(*oper.tokentypes_support_sub), 1, args)

    if (modifier_vl := safe_getv(modifier_tok, modified_var.type)) == None:
        return errors.SCLError(f"Expected argument of type '{modified_var.type.name}' at position 3")
    modified_var.set_value(modified_var.get_value() - modifier_vl)

def mul_f(args: list[Token]):
    modified_tok = ps.try_get([TokenType.IDT], 0, args)

    if not (modified_var := ev.get_from_id(modified_tok.value)):
        return errors.SCLNotFoundError(modified_tok.value)
    if not modified_var.type in oper.datatypes_support_mul:
        return errors.SCLWrongOperationError("multiplication", modified_var.type.name)
    modifier_tok = ps.try_get(commands.make_value(*oper.tokentypes_support_mul), 1, args)

    if (modifier_vl := safe_getv(modifier_tok, modified_var.type)) == None:
        return errors.SCLError(f"Expected argument of type '{modified_var.type.name}' at position 3")
    modified_var.set_value(modified_var.get_value() * modifier_vl)

def div_f(args: list[Token]):
    modified_tok = ps.try_get([TokenType.IDT], 0, args)

    if not (modified_var := ev.get_from_id(modified_tok.value)):
        return errors.SCLNotFoundError(modified_tok.value)
    if not modified_var.type in oper.datatypes_support_div:
        return errors.SCLWrongOperationError("division", modified_var.type.name)
    modifier_tok = ps.try_get(commands.make_value(*oper.tokentypes_support_div), 1, args)

    if (modifier_vl := safe_getv(modifier_tok, modified_var.type)) == None:
        return errors.SCLError(f"Expected argument of type '{modified_var.type.name}' at position 3")
    if modifier_vl == 0:
        return errors.SCLDivisionByZeroError(modified_var.ident)
    if modified_var.type == al.DT_TYPES.INT:
        modified_var.set_value(modified_var.get_value() // modifier_vl)
    else:
        modified_var.set_value(modified_var.get_value() / modifier_vl)

def pow_f(args: list[Token]):
    modified_tok = ps.try_get([TokenType.IDT], 0, args)

    if not (modified_var := ev.get_from_id(modified_tok.value)):
        return errors.SCLNotFoundError(modified_tok.value)
    if not modified_var.type in oper.datatypes_support_pow:
        return errors.SCLWrongOperationError("power", modified_var.type.name)
    modifier_tok = ps.try_get(commands.make_value(*oper.tokentypes_support_pow), 1, args)

    if (modifier_vl := safe_getv(modifier_tok, modified_var.type)) == None:
        return errors.SCLError(f"Expected argument of type '{modified_var.type.name}' at position 3")
    modified_var.set_value(modified_var.get_value() ** modifier_vl)

def help_f(args: list[Token]):
    cmd_tok = ps.try_get([TokenType.IDT], 0, args)
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
        case 'arr':
            print(manuals.ARR)
        case 'get':
            print(manuals.GET)
        case 'mod':
            print(manuals.MOD)
        case 'len':
            print(manuals.LEN)
        case 'foreach':
            print(manuals.FOREACH)
        case 'if':
            print(manuals.IF)
        case 'alias':
            print(manuals.ALIAS)
        case 'list':
            print("dp, dpl, loop, new, set, stt, end, clr, del, exec, add, sub, mul, div, pow, help, fun, ret, call, read, arr, get, mod, len, foreach, if, alias")
        case _:
            return errors.SCLError("Unknown Command, either it does not exist or there is no manual for it")

def fun_f(args: list[Token]):
    type_tok = ps.try_get([TokenType.IDT], 0, args)

    if not type_tok.has_specific_value(kws.return_datatypes):
        return errors.SCLError(f"Syntax Error: expected argument with specific value in {kws.return_datatypes}, got {type_tok.value}")
    ftype: al.DT_TYPES = al.DT_TYPES.str_to_type(type_tok.value)
    name_tok = ps.try_get([TokenType.IDT], 1, args)

    name :str = name_tok.value
    params_tok = ps.try_get([TokenType.TUPLE], 2, args)

    params = ps.check_formal_parameters(params_tok) if not params_tok.is_empty_tuple() else None

    body_tok = ps.try_get([TokenType.BODY],3,args)

    body = body_tok.value
    ev.alloc(al.Function(ftype,name,params,body))

def call_f(args: list[Token]):
    name_tok = ps.try_get([TokenType.IDT], 0, args)

    fun = ev.get_from_id(name_tok.value)
    if not type(fun) is al.Function:
        return errors.SCLNotCallableError(name_tok.value)
    effective_params_tok = ps.try_get([TokenType.TUPLE], 1, args)
    eff_params = ps.check_effective_param(effective_params_tok)
    return fun.execute_fun(eff_params)


def ret_f(args: list[Token]):
    vtok = ps.try_get(commands.make_value(*parser.tokens.all_literals()), 0, args)

    if vtok.type == TokenType.VARRF:
        if (val := ul.var_ref(vtok.value).get_value()) != None:
            ev.CURENV.fun_ret = val
    else:
        ev.CURENV.fun_ret = vtok.evaluate()

def read_f(args: list[Token]):
    vartok = ps.try_get([TokenType.IDT], 0, args)

    if not (var := ul.var_ref(vartok.value)):
        return errors.SCLNotFoundError(vartok.value)
    usr_input = input()
    if var.type.is_compatible_with_type(usr_input):
        var.set_value(var.type.convert_str_to_value(usr_input))
    else:
        return errors.SCLWrongTypeError(var.type.name)

def array_f(args: list[Token]):
    oper_tok = ps.try_get([TokenType.IDT], 0, args)
    if oper_tok.has_specific_value("new"):
        type_tok = ps.try_get([TokenType.IDT], 1, args)
        if type_tok.has_specific_value(kws.arr_types):
            name_tok = ps.try_get([TokenType.IDT], 2, args)
            if ul.is_valid_name(name_tok.value):
                values_tok = ps.try_get(make_value(TokenType.ARR),3,args)
                values = strict_getv(values_tok,al.DT_TYPES.str_to_type(type_tok.value),isarray=True)
                replace_varrf_by_value(values)
                new_arr = al.Array(
                        al.DT_TYPES.str_to_type(type_tok.value),
                        name_tok.value,
                        values
                    )
                if type_tok.value != 'any':
                    if not new_arr.are_values_compatible_with_type(values):
                        return errors.SCLError(f"Not all values are compatible with the array type: {new_arr.type.name}")
                ev.alloc(
                    new_arr
                )
            else:
                return errors.SCLInvalidIdentError(name_tok.value)
        else:
            return errors.SCLUnknownTypeError(type_tok.value)
    else:
        return errors.SCLError(f"Syntax Error: expected argument with specific value in {kws.arr_opts}, got {oper_tok.value}")

def get_f(args: list[Token]):
    iter_tok = ps.try_get([TokenType.IDT], 0, args)
    iter = ev.get_from_id(iter_tok.value)
    if not issubclass(type(iter),al.Iterable):
        return errors.SCLNotIterableError(iter_tok.value)
    idx_tok = ps.try_get(make_value(TokenType.INT),1,args)
    idx = strict_getv(idx_tok,al.DT_TYPES.INT)
    dest_tok = ps.try_get([TokenType.IDT], 2, args)
    dest = ev.get_from_id(dest_tok.value)
    if iter.type == DT_TYPES.ANY:
        idxth = iter.get_at_index(idx) # the i^th element
        idxth_type = DT_TYPES.guess_type(str(idxth))
        if idxth_type == dest.type:
            dest.set_value(idxth)
        else:
            return errors.SCLWrongTypeError(idxth_type.name,dest.type.name)
    elif dest.type != iter.type:
        return errors.SCLWrongTypeError(iter.type.name,dest.type.name)
    dest.set_value(iter.get_at_index(idx))

def mod_f(args: list[Token]):
    iter_tok = ps.try_get([TokenType.IDT], 0, args)
    iter = ev.get_from_id(iter_tok.value)
    if not issubclass(type(iter), al.Iterable):
        return errors.SCLNotIterableError(iter_tok.value)
    idx_tok = ps.try_get(make_value(TokenType.INT), 1, args)
    idx = strict_getv(idx_tok, al.DT_TYPES.INT)
    if iter.type != al.DT_TYPES.ANY:
        new_v_tok = ps.try_get(commands.make_value(iter.type.get_literal_version()), 2, args)
        new_v = strict_getv(new_v_tok, iter.type)
    else:
        new_v_tok = ps.try_get(commands.make_value(*parser.tokens.all_literals()), 2, args)
        if new_v_tok.type == TokenType.VARRF:
            new_v = ul.var_ref(new_v_tok.value).get_value()
        else:
            new_v = al.DT_TYPES.guess_type(new_v_tok.value).convert_str_to_value(new_v_tok.value)
    iter.set_at_index(idx,new_v)

def len_f(args: list[Token]):
    iter_tok = ps.try_get([TokenType.IDT], 0, args)
    iter = ev.get_from_id(iter_tok.value)
    if not issubclass(type(iter), al.Iterable):
        return errors.SCLNotIterableError(iter_tok.value)
    dest_tok = ps.try_get([TokenType.IDT], 1, args)
    dest = ev.get_from_id(dest_tok.value)
    if dest.type != al.DT_TYPES.INT:
        return errors.SCLWrongTypeError(al.DT_TYPES.INT.__repr__(), dest.type.name)
    dest.set_value(iter.length)

def foreach_f(args: list[Token]):
    element_ident = ps.try_get([TokenType.IDT], 0, args).value
    in_kw_tok = ps.try_get([TokenType.IDT], 1, args)
    if not in_kw_tok.has_specific_value(kws.foreach_opts):
        return errors.SCLError(f"Syntax Error: expected argument with specific value in {kws.foreach_opts}, got {in_kw_tok.value}")
    iter_tok = ps.try_get([TokenType.IDT], 2, args)
    iter = ev.get_from_id(iter_tok.value)
    if not issubclass(type(iter),al.Iterable):
        if not hasattr(iter.get_value(),'__iter__'):
            return errors.SCLNotIterableError(iter_tok.value)
        iter = al.Iterable(iter.get_value())
    body_tok = ps.try_get([TokenType.BODY],3,args)
    instructions = body_tok.value

    element = al.Variable(al.VARKIND.MUT,al.DT_TYPES.ANY,element_ident,None)
    fore_exec = Executor()
    ev.alloc(
        element
    )
    for e in iter.get_items_gen():
        element.set_value(e)
        for ins in instructions:
            fore_exec.execute(ins)
    ev.de_alloc(
        element
    )

def if_f(args: list[Token]):
    bool_expr_tok = ps.try_get([TokenType.BLEXP],0,args)
    true_section_tok = ps.try_get([TokenType.BODY],1,args)
    false_section_tok = ps.try_get([TokenType.BODY],2,args)

    if_exec = Executor()
    if (eval_bool_expr(bool_expr_tok.value)):
        for ins in true_section_tok.value:
            if_exec.execute(ins)
    else:
        for ins in false_section_tok.value:
            if_exec.execute(ins)

def alias_f(args: list[Token]):
    opt_tok = ps.try_get([TokenType.IDT],0,args)
    if not opt_tok.has_specific_value(kws.alias_opts):
        return errors.SCLError(f"Syntax Error: expected argument with specific value in {kws.alias_opts}, got {opt_tok.value}")
    alias_name_tok = ps.try_get([TokenType.IDT],1,args)

    if opt_tok.value == "create":
        alias_content_tok = ps.try_get([TokenType.STR], 2, args)
        ev.CURENV.aliases[alias_name_tok.value] = alias_content_tok.value
    else:
        del ev.CURENV.aliases[alias_name_tok.value]