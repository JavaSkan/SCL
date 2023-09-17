import os
import ulang as ul
import allocable as al
import env as ev
import manuals
import TuiErrors as terr

def display_f(args):
	try:
		res = ""
		add = ""
		for i,arg in enumerate(args):
			add = ul.var_ref(arg)
			res += add
			res += " " if i != len(args)-1 else " "
		print(res,end="")
	except IndexError:
		terr.TuiArgsMismatchError().trigger()

def displayl_f(args):
	try:
		display_f(args)
		print()
	except IndexError:
		terr.TuiArgsMismatchError().trigger()


def loop_f(args):
	insts = ul.parse_body(args[1])
	for i in range(int(ul.var_ref(args[0]))):
		for ins in insts:
			if type(ins) is str:
				ul.execute(ins)
			else:
				ul.execute_block(ins)


def new_f(args):
	if not ul.is_valid_name(args[1]):
		terr.TuiInvalidNameError(args[1]).trigger()

	match args[0]:
		case "str":
			al.Variable(al.DT_TYPES.STR, args[1], ul.var_ref(" ".join(args[2:])))
		case "int":
			if not (str_int_value := ul.var_ref("".join(args[2:]))).isdigit():
				terr.TuiWrongTypeError("int").trigger()
			al.Variable(al.DT_TYPES.INT,args[1],int(str_int_value))
		case "flt":
			if not (str_int_value := ul.var_ref("".join(args[2:]))).replace('.','',1).isdigit():
				terr.TuiWrongTypeError("float").trigger()
			al.Variable(al.DT_TYPES.FLT, args[1], float(str_int_value))
		case "arr":
			al.Array(args[1], ul.parse_arr(args[2]))
		case _:
			terr.TuiError(f"Unknown type {args[0]}").trigger()


def state_f(args):
	print(f"ALLOCATIONS : {ev._VARS}")
	print(f"BOOL_STATE : {ev._BOOL}")
	print(f"FUNCTION RETURN VALUE : {ev._FUN_RET}")
	print(f"VARIABLE REFERENCING SYMBOL : {ev._VARREF_SYM}")
	print(f"ERR_QUIT:{ev._ERR_QUIT}")

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
			terr.TuiError("Unknown End Error Signal").trigger()
	ev._VARS.clear()
	quit()

def clear_f(args):
	ev._VARS.clear()

def delete_f(args):
	ev._VARS.pop(ev._VARS.index(ev.get_from_id(args[0])))

def set_f(args):
	if (var := ev.get_from_id(args[0])) == None:
		terr.TuiNotFoundError(args[0]).trigger()
	new = ev.get_from_id(args[1][1:]) if ul.is_var_ref(args[1]) else args[1]
	if type(new) is str:
		if var.is_compatible_with_type(new):
			var.set_value(var.convert_str_value_to_type(new))
		else:
			terr.TuiWrongTypeError(var.type.__repr__()).trigger()
	else:
		if var.type == new.type:
			var.set_value(new.get_value())
		else:
			terr.TuiWrongTypeError(var.type.__repr__(),new.type.__repr__()).trigger()

def execute_f(args):
	if os.path.exists(args[0]):
		if args[0].endswith(".tui"):
			with open(args[0],"r") as f:
				lines = f.read().split("\n")
				for line in lines:
					ul.execute(line)
		else:
			terr.TuiError("Incorrect file extension").trigger()
	else:
		terr.TuiError("There is not such file").trigger()

def add_f(args):
	if (var1 := ev.get_from_id(args[0])) == None:
		terr.TuiNotFoundError(args[0]).trigger()
	var2 = ev.get_from_id(args[1][1:]) if ul.is_var_ref(args[1]) else args[1]
	if type(var1) is al.Array:
		var1.add_v(var2)
		return
	if type(var2) is str:
		if var1.is_compatible_with_type(var2):
			var1.set_value(var1.get_value() + var1.convert_str_value_to_type(var2))
		else:
			terr.TuiWrongTypeError(var1.type.__repr__()).trigger()
	else:
		if var2 == None:
			terr.TuiNotFoundError(args[1]).trigger()
		if var1.is_compatible_with_type(str(var2.get_value())):
			var1.set_value(var1.get_value() + var2.get_value())
		else:
			terr.TuiWrongTypeError(var1.type.__repr__(),var2.type.__repr__()).trigger()


def sub_f(args):
	if (var1 := ev.get_from_id(args[0])) == None:
		terr.TuiNotFoundError(args[0]).trigger()
	var2 = ev.get_from_id(args[1][1:]) if ul.is_var_ref(args[1]) else args[1]
	if type(var1) is al.Array:
		terr.TuiWrongOperationError("subtraction","array")
		return
	if type(var2) is str:
		if var1.is_compatible_with_type(var2):
			if var1.type in (al.DT_TYPES.INT,al.DT_TYPES.FLT):
				var1.set_value(var1.get_value() - var1.convert_str_value_to_type(var2))
			else:
				terr.TuiWrongOperationError("subtraction",var1.type.__repr__()).trigger()
		else:
			terr.TuiWrongTypeError(var1.type.__repr__()).trigger()
	else:
		if var2 == None:
			terr.TuiNotFoundError(args[1]).trigger()
		if var1.is_compatible_with_type(str(var2.get_value())):
			if var1.type in (al.DT_TYPES.INT, al.DT_TYPES.FLT):
				var1.set_value(var1.get_value() - var2.get_value())
			else:
				terr.TuiWrongOperationError("subtraction", var1.type.__repr__()).trigger()
		else:
			terr.TuiWrongTypeError(var1.type.__repr__(),var2.type.__repr__()).trigger()

def mul_f(args):
	if (var1 := ev.get_from_id(args[0])) == None:
		terr.TuiNotFoundError(args[0]).trigger()
	var2 = ev.get_from_id(args[1][1:]) if ul.is_var_ref(args[1]) else args[1]
	if type(var1) is al.Array:
		terr.TuiWrongOperationError("multiplication", "array")
		return
	if type(var2) is str:
		if var1.is_compatible_with_type(var2):
			if var1.type in (al.DT_TYPES.INT, al.DT_TYPES.FLT):
				var1.set_value(var1.get_value() * var1.convert_str_value_to_type(var2))
			else:
				terr.TuiWrongOperationError("multiplication", var1.type.__repr__()).trigger()
		else:
			terr.TuiWrongTypeError(var1.type.__repr__()).trigger()
	else:
		if var2 == None:
			terr.TuiNotFoundError(args[1]).trigger()
		if var1.is_compatible_with_type(str(var2.get_value())):
			if var1.type in (al.DT_TYPES.INT, al.DT_TYPES.FLT):
				var1.set_value(var1.get_value() * var2.get_value())
			else:
				terr.TuiWrongOperationError("multiplication", var1.type.__repr__()).trigger()
		else:
			terr.TuiWrongTypeError(var1.type.__repr__(), var2.type.__repr__()).trigger()

def div_f(args):
	if (var1 := ev.get_from_id(args[0])) == None:
		terr.TuiNotFoundError(args[0]).trigger()
	var2 = ev.get_from_id(args[1][1:]) if ul.is_var_ref(args[1]) else args[1]
	if type(var1) is al.Array:
		terr.TuiWrongOperationError("division", "array")
		return
	if type(var2) is str:
		if var1.is_compatible_with_type(var2):
			if float(var2) == 0.0:
				terr.TuiDivisionByZeroError(var1.id).trigger()
			if var1.type == al.DT_TYPES.INT:
				var1.set_value(var1.get_value() // var1.convert_str_value_to_type(var2))
			elif var1.type == al.DT_TYPES.FLT:
				var1.set_value(var1.get_value() / var1.convert_str_value_to_type(var2))
			else:
				terr.TuiWrongOperationError("division", var1.type.__repr__()).trigger()
		else:
			terr.TuiWrongTypeError(var1.type.__repr__()).trigger()
	else:
		if var2 == None:
			terr.TuiNotFoundError(args[1]).trigger()
		if var1.is_compatible_with_type(str(var2.get_value())):
			if var2.get_value() == 0.0:
				terr.TuiDivisionByZeroError(var1.id).trigger()
			if var1.type == al.DT_TYPES.INT:
				var1.set_value(var1.get_value() // var2.get_value())
			elif var1.type == al.DT_TYPES.FLT:
				var1.set_value(var1.get_value() / var2.get_value())
			else:
				terr.TuiWrongOperationError("division", var1.type.__repr__()).trigger()
		else:
			terr.TuiWrongTypeError(var1.type.__repr__(), var2.type.__repr__()).trigger()

def pow_f(args):
	if (var1 := ev.get_from_id(args[0])) == None:
		terr.TuiNotFoundError(args[0]).trigger()
	var2 = ev.get_from_id(args[1][1:]) if ul.is_var_ref(args[1]) else args[1]
	if type(var1) is al.Array:
		terr.TuiWrongOperationError("power", "array")
		return
	if type(var2) is str:
		if var1.is_compatible_with_type(var2):
			if var1.type in (al.DT_TYPES.INT, al.DT_TYPES.FLT):
				var1.set_value(var1.get_value() ** var1.convert_str_value_to_type(var2))
			else:
				terr.TuiWrongOperationError("power", var1.type.__repr__()).trigger()
		else:
			terr.TuiWrongTypeError(var1.type.__repr__()).trigger()
	else:
		if var2 == None:
			terr.TuiNotFoundError(args[1]).trigger()
		if var1.is_compatible_with_type(str(var2.get_value())):
			if var1.type in (al.DT_TYPES.INT, al.DT_TYPES.FLT):
				var1.set_value(var1.get_value() ** var2.get_value())
			else:
				terr.TuiWrongOperationError("power", var1.type.__repr__()).trigger()
		else:
			terr.TuiWrongTypeError(var1.type.__repr__(), var2.type.__repr__()).trigger()

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
		case 'enable_eq':
			print(manuals.ENABLE_EQ)
		case 'disable_eq':
			print(manuals.DISABLE_EQ)
		case 'read':
			print(manuals.READ)
		case 'list':
			print("dp, dpl, loop, new, set, stt, end, clr, del, exec, add, sub, mu, div, pow, help, fun, ret, vr, call, enable_eq, disable_eq, read")
		case _:
			terr.TuiError("Unknown Command, either it does not exist or there is no manual for it").trigger()

def fun_f(args):
	if not ul.is_valid_name(args[0]):
		terr.TuiInvalidNameError(args[0]).trigger()

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
		terr.TuiError(f'{args[0]} is not a valid argument for this command').trigger()

def call_f(args):
	if (fun := ev.get_from_id(args[0])) == None:
		terr.TuiNotFoundError(args[0]).trigger()
	if type(fun) is not al.Function:
		terr.TuiNotCallableError(args[0]).trigger()
	fun.execute_fun(args[1:])

def enable_err_quit_f(args):
	ev._ERR_QUIT = True

def disable_err_quit_f(args):
	ev._ERR_QUIT = False

def read_f(args):
	if (var := ev.get_from_id(args[0])) == None:
		terr.TuiNotFoundError(args[0]).trigger()
	user_input = input("")
	if var.is_compatible_with_type(user_input):
		var.set_value(var.convert_str_value_to_type(user_input))
	else:
		terr.TuiWrongTypeError(var.type.__repr__()).trigger()
