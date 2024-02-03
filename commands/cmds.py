import os

from parser import parsing as tp, keywords as kws, errors as err
from runtime import allocable as al, env as ev, ulang as ul
import manuals


def display_f(args: list[tp.ParseToken]):
	for i,arg in enumerate(args):
		print(arg.value,end=(" " if i < len(args)-1 else ""))

def displayl_f(args: list[tp.ParseToken]):
	try:
		display_f(args)
		print()
	except IndexError:
		return err.SCLArgsMismatchError()


def loop_f(args: list[tp.ParseToken]):
	it_tok, err = tp.try_get([tp.TokenType.VARREF,tp.TokenType.INTLIT],0,args)
	if err:
		return err
	it = 0
	if it_tok.type == tp.TokenType.VARREF:
		it = int(ul.var_ref(it_tok.value))
	else:
		it = int(it_tok.value)
	del it_tok
	body_tok, err = tp.try_get([tp.TokenType.BODY],1,args)
	if err:
		return err
	instructions = tp.parse_body(body_tok.value)
	del body_tok
	for i in range(it):
		for ins in instructions:
			ul.execute(ins)


def new_f(args: list[tp.ParseToken]):
	type_tok, err = tp.try_get([tp.TokenType.ARG],0,args)
	if err:
		return err
	var_name_tok, err = tp.try_get([tp.TokenType.ARG],1,args)
	if err:
		return err
	if not ul.is_valid_name(var_name_tok.value):
		return err.SCLInvalidNameError(var_name_tok.value)
	del var_name_tok
	if not (_type := kws.data_types_keywords.get(type_tok.value)):
		return err.SCLUnknownTypeError(type_tok.value)
	value_tok, err = tp.try_get([_type,tp.TokenType.VARREF],2,args)
	if err:
		return err
	if value_tok.type == tp.TokenType.VARREF:
		pass
	#TODO type checking of variable referencing, same for loop command



def state_f(args):
	print(f"ALLOCATIONS : {ev._VARS}")
	print(f"BOOL_STATE : {ev._BOOL}")
	print(f"FUNCTION RETURN VALUE : {ev._FUN_RET}")
	print(f"VARIABLE REFERENCING SYMBOL : {ev._VARREF_SYM}")

def end_f(args):
	if (alen := len(args)) != 0:
		if (fst_arg := ul.var_ref(args[0])) == "0":
			if alen == 2:
				if ul.var_ref(args[1]) == "1":
					print("ended successfully")
		elif fst_arg == "1":
			if alen == 2:
				if ul.var_ref(args[1]) == "1":
					print("ended with a failure")
		else:
			err.SCLError("Unknown End Error Signal").trigger()
	ev._VARS.clear()
	quit()

def clear_f(args):
	ev._VARS.clear()

def delete_f(args):
	ev._VARS.pop(ev._VARS.index(ev.get_from_id(args[0])))

def set_f(args):
	if (var := ev.get_from_id(args[0])) == None:
		err.SCLNotFoundError(args[0]).trigger()
	new = ev.get_from_id(args[1][1:]) if ul.is_var_ref(args[1]) else args[1]
	if type(new) is str:
		if var.is_compatible_with_type(new):
			var.set_value(var.convert_str_value_to_type(new))
		else:
			err.SCLWrongTypeError(var.type.__repr__()).trigger()
	else:
		if var.type == new.type:
			var.set_value(new.get_value())
		else:
			err.SCLWrongTypeError(var.type.__repr__(),new.type.__repr__()).trigger()

def execute_f(args):
	if os.path.exists(args[0]):
		if args[0].endswith(".scl"):
			with open(args[0],"r") as f:
				lines = f.read().split("\n")
				for line in lines:
					ul.execute(line)
		else:
			err.SCLError("Incorrect file extension").trigger()
	else:
		err.SCLError("There is not such file").trigger()

def add_f(args):
	if (var1 := ev.get_from_id(args[0])) == None:
		err.SCLNotFoundError(args[0]).trigger()
	var2 = ev.get_from_id(args[1][1:]) if ul.is_var_ref(args[1]) else args[1]
	if type(var1) is al.Array:
		var1.add_v(var2)
		return
	if type(var2) is str:
		if var1.is_compatible_with_type(var2):
			var1.set_value(var1.get_value() + var1.convert_str_value_to_type(var2))
		else:
			err.SCLWrongTypeError(var1.type.__repr__()).trigger()
	else:
		if var2 == None:
			err.SCLNotFoundError(args[1]).trigger()
		if var1.is_compatible_with_type(str(var2.get_value())):
			var1.set_value(var1.get_value() + var2.get_value())
		else:
			err.SCLWrongTypeError(var1.type.__repr__(),var2.type.__repr__()).trigger()


def sub_f(args):
	if (var1 := ev.get_from_id(args[0])) == None:
		err.SCLNotFoundError(args[0]).trigger()
	var2 = ev.get_from_id(args[1][1:]) if ul.is_var_ref(args[1]) else args[1]
	if type(var1) is al.Array:
		err.SCLWrongOperationError("subtraction","array")
		return
	if type(var2) is str:
		if var1.is_compatible_with_type(var2):
			if var1.type in (al.DT_TYPES.INT,al.DT_TYPES.FLT):
				var1.set_value(var1.get_value() - var1.convert_str_value_to_type(var2))
			else:
				err.SCLWrongOperationError("subtraction",var1.type.__repr__()).trigger()
		else:
			err.SCLWrongTypeError(var1.type.__repr__()).trigger()
	else:
		if var2 == None:
			err.SCLNotFoundError(args[1]).trigger()
		if var1.is_compatible_with_type(str(var2.get_value())):
			if var1.type in (al.DT_TYPES.INT, al.DT_TYPES.FLT):
				var1.set_value(var1.get_value() - var2.get_value())
			else:
				err.SCLWrongOperationError("subtraction", var1.type.__repr__()).trigger()
		else:
			err.SCLWrongTypeError(var1.type.__repr__(),var2.type.__repr__()).trigger()

def mul_f(args):
	if (var1 := ev.get_from_id(args[0])) == None:
		err.SCLNotFoundError(args[0]).trigger()
	var2 = ev.get_from_id(args[1][1:]) if ul.is_var_ref(args[1]) else args[1]
	if type(var1) is al.Array:
		err.SCLWrongOperationError("multiplication", "array")
		return
	if type(var2) is str:
		if var1.is_compatible_with_type(var2):
			if var1.type in (al.DT_TYPES.INT, al.DT_TYPES.FLT):
				var1.set_value(var1.get_value() * var1.convert_str_value_to_type(var2))
			else:
				err.SCLWrongOperationError("multiplication", var1.type.__repr__()).trigger()
		else:
			err.SCLWrongTypeError(var1.type.__repr__()).trigger()
	else:
		if var2 == None:
			err.SCLNotFoundError(args[1]).trigger()
		if var1.is_compatible_with_type(str(var2.get_value())):
			if var1.type in (al.DT_TYPES.INT, al.DT_TYPES.FLT):
				var1.set_value(var1.get_value() * var2.get_value())
			else:
				err.SCLWrongOperationError("multiplication", var1.type.__repr__()).trigger()
		else:
			err.SCLWrongTypeError(var1.type.__repr__(), var2.type.__repr__()).trigger()

def div_f(args):
	if (var1 := ev.get_from_id(args[0])) == None:
		err.SCLNotFoundError(args[0]).trigger()
	var2 = ev.get_from_id(args[1][1:]) if ul.is_var_ref(args[1]) else args[1]
	if type(var1) is al.Array:
		err.SCLWrongOperationError("division", "array")
		return
	if type(var2) is str:
		if var1.is_compatible_with_type(var2):
			if float(var2) == 0.0:
				err.SCLDivisionByZeroError(var1.id).trigger()
			if var1.type == al.DT_TYPES.INT:
				var1.set_value(var1.get_value() // var1.convert_str_value_to_type(var2))
			elif var1.type == al.DT_TYPES.FLT:
				var1.set_value(var1.get_value() / var1.convert_str_value_to_type(var2))
			else:
				err.SCLWrongOperationError("division", var1.type.__repr__()).trigger()
		else:
			err.SCLWrongTypeError(var1.type.__repr__()).trigger()
	else:
		if var2 == None:
			err.SCLNotFoundError(args[1]).trigger()
		if var1.is_compatible_with_type(str(var2.get_value())):
			if var2.get_value() == 0.0:
				err.SCLDivisionByZeroError(var1.id).trigger()
			if var1.type == al.DT_TYPES.INT:
				var1.set_value(var1.get_value() // var2.get_value())
			elif var1.type == al.DT_TYPES.FLT:
				var1.set_value(var1.get_value() / var2.get_value())
			else:
				err.SCLWrongOperationError("division", var1.type.__repr__()).trigger()
		else:
			err.SCLWrongTypeError(var1.type.__repr__(), var2.type.__repr__()).trigger()

def pow_f(args):
	if (var1 := ev.get_from_id(args[0])) == None:
		err.SCLNotFoundError(args[0]).trigger()
	var2 = ev.get_from_id(args[1][1:]) if ul.is_var_ref(args[1]) else args[1]
	if type(var1) is al.Array:
		err.SCLWrongOperationError("power", "array")
		return
	if type(var2) is str:
		if var1.is_compatible_with_type(var2):
			if var1.type in (al.DT_TYPES.INT, al.DT_TYPES.FLT):
				var1.set_value(var1.get_value() ** var1.convert_str_value_to_type(var2))
			else:
				err.SCLWrongOperationError("power", var1.type.__repr__()).trigger()
		else:
			err.SCLWrongTypeError(var1.type.__repr__()).trigger()
	else:
		if var2 == None:
			err.SCLNotFoundError(args[1]).trigger()
		if var1.is_compatible_with_type(str(var2.get_value())):
			if var1.type in (al.DT_TYPES.INT, al.DT_TYPES.FLT):
				var1.set_value(var1.get_value() ** var2.get_value())
			else:
				err.SCLWrongOperationError("power", var1.type.__repr__()).trigger()
		else:
			err.SCLWrongTypeError(var1.type.__repr__(), var2.type.__repr__()).trigger()

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
			err.SCLError("Unknown Command, either it does not exist or there is no manual for it").trigger()

def fun_f(args):
	if not ul.is_valid_name(args[0]):
		err.SCLInvalidNameError(args[0]).trigger()

	#fun <name> {body}
	if (alen := len(args)) == 2:
		al.Function(args[0],None,ul.parse_body(args[1]))
	#fun <name> (params) {body}
	elif alen == 3:
		al.Function(args[0],ul.parse_params(args[1]),ul.parse_body(args[2]))

def ret_f(args):
	ev._FUN_RET = ul.var_ref(args[0])

def vr_f(args):
	if args[0] == 'set':
		ev._VARREF_SYM = args[1]
	elif args[0] == 'reset':
		ev._VARREF_SYM = '$'
	else:
		err.SCLError(f'{args[0]} is not a valid argument for this command').trigger()

def call_f(args):
	if (fun := ev.get_from_id(args[0])) == None:
		err.SCLNotFoundError(args[0]).trigger()
	if type(fun) is not al.Function:
		err.SCLNotCallableError(args[0]).trigger()
	fun.execute_fun(args[1:])

def read_f(args):
	if (var := ev.get_from_id(args[0])) == None:
		err.SCLNotFoundError(args[0]).trigger()
	user_input = input("")
	if var.is_compatible_with_type(user_input):
		var.set_value(var.convert_str_value_to_type(user_input))
	else:
		err.SCLWrongTypeError(var.type.__repr__()).trigger()
