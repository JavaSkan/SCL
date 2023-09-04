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
	ev.get_from_id(args[0]).vl = ul.var_ref(args[1])

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
	if (var := ev.get_from_id(args[0])) == None:
		terr.TuiNotFoundError(args[0]).trigger()
	added = ev.get_from_id(args[1][1:]) if ul.is_var_ref(args[1]) else args[1]
	if type(var) is al.Array:
		var.add_v(added)
		return
	match var.type:
		case al.DT_TYPES.INT:
			if type(added) is al.Variable:
				if added.type is al.DT_TYPES.INT:
					var.vl = var.get_value() + added.get_value()
				else:
					terr.TuiWrongTypeError("int", added.type.to_python_type().__class__.__name__).trigger()
			else:
				if added.isdigit():
					var.vl = var.get_value() + int(added)
				else:
					terr.TuiWrongTypeError("int").trigger()
		case al.DT_TYPES.FLT:
			if type(added) is al.Variable:
				if added.isdigit() or added.replace('.', '', 1).isdigit():
					var.vl = var.get_value() + float(added.get_value())
				else:
					terr.TuiWrongTypeError("flt",added.type.to_python_type().__class__.__name__).trigger()
			else:
				if added.isdigit() or added.replace('.', '', 1).isdigit():
					var.vl = var.get_value() + float(added)
				else:
					terr.TuiWrongTypeError("flt").trigger()
		case al.DT_TYPES.STR:
			if type(added) is al.Variable:
				var.vl = var.get_value() + str(added.get_value())
			else:
				var.vl = var.get_value() + added


def sub_f(args):
	if (var := ev.get_from_id(args[0])) == None:
		terr.TuiNotFoundError(args[0]).trigger()
	added = ev.get_from_id(args[1][1:]) if ul.is_var_ref(args[1]) else args[1]
	if type(var) is al.Array:
		terr.TuiWrongOperationError("subtraction","array")
	match var.type:
		case al.DT_TYPES.INT:
			if type(added) is al.Variable:
				if added.type is al.DT_TYPES.INT:
					var.vl = var.get_value() - added.get_value()
				else:
					terr.TuiWrongTypeError("int", added.type.to_python_type().__class__.__name__).trigger()
			else:
				if added.isdigit():
					var.vl = var.get_value() - int(added)
				else:
					terr.TuiWrongTypeError("int").trigger()
		case al.DT_TYPES.FLT:
			if type(added) is al.Variable:
				if added.isdigit() or added.replace('.', '', 1).isdigit():
					var.vl = var.get_value() - float(added.get_value())
				else:
					terr.TuiWrongTypeError("flt", added.type.to_python_type().__class__.__name__).trigger()
			else:
				if added.isdigit() or added.replace('.', '', 1).isdigit():
					var.vl = var.get_value() - float(added)
				else:
					terr.TuiWrongTypeError("flt").trigger()
		case al.DT_TYPES.STR:
			terr.TuiWrongOperationError("subtraction","str")

def mul_f(args):
	if (var := ev.get_from_id(args[0])) == None:
		terr.TuiNotFoundError(args[0]).trigger()
	added = ev.get_from_id(args[1][1:]) if ul.is_var_ref(args[1]) else args[1]
	if type(var) is al.Array:
		terr.TuiWrongOperationError("multiplication", "array")
	match var.type:
		case al.DT_TYPES.INT:
			if type(added) is al.Variable:
				if added.type is al.DT_TYPES.INT:
					var.vl = var.get_value() * added.get_value()
				else:
					terr.TuiWrongTypeError("int", added.type.to_python_type().__class__.__name__).trigger()
			else:
				if added.isdigit():
					var.vl = var.get_value() * int(added)
				else:
					terr.TuiWrongTypeError("int").trigger()
		case al.DT_TYPES.FLT:
			if type(added) is al.Variable:
				if added.isdigit() or added.replace('.', '', 1).isdigit():
					var.vl = var.get_value() * float(added.get_value())
				else:
					terr.TuiWrongTypeError("flt", added.type.to_python_type().__class__.__name__).trigger()
			else:
				if added.isdigit() or added.replace('.', '', 1).isdigit():
					var.vl = var.get_value() * float(added)
				else:
					terr.TuiWrongTypeError("flt").trigger()
		case al.DT_TYPES.STR:
			terr.TuiWrongOperationError("multiplication", "str")

def div_f(args):
	if (var := ev.get_from_id(args[0])) == None:
		terr.TuiNotFoundError(args[0]).trigger()
	added = ev.get_from_id(args[1][1:]) if ul.is_var_ref(args[1]) else args[1]
	if type(var) is al.Array:
		terr.TuiWrongOperationError("division", "array")
	match var.type:
		case al.DT_TYPES.INT:
			if type(added) is al.Variable:
				if added.type is al.DT_TYPES.INT:
					var.vl = int(var.get_value() / added.get_value())
				else:
					terr.TuiWrongTypeError("int", added.type.to_python_type().__class__.__name__).trigger()
			else:
				if added.isdigit():
					var.vl = int(var.get_value() / int(added))
				else:
					terr.TuiWrongTypeError("int").trigger()
		case al.DT_TYPES.FLT:
			if type(added) is al.Variable:
				if added.isdigit() or added.replace('.', '', 1).isdigit():
					var.vl = var.get_value() / float(added.get_value())
				else:
					terr.TuiWrongTypeError("flt", added.type.to_python_type().__class__.__name__).trigger()
			else:
				if added.isdigit() or added.replace('.', '', 1).isdigit():
					var.vl = var.get_value() / float(added)
				else:
					terr.TuiWrongTypeError("flt").trigger()
		case al.DT_TYPES.STR:
			terr.TuiWrongOperationError("division", "str")

def pow_f(args):
	if (var := ev.get_from_id(args[0])) == None:
		terr.TuiNotFoundError(args[0]).trigger()
	added = ev.get_from_id(args[1][1:]) if ul.is_var_ref(args[1]) else args[1]
	if type(var) is al.Array:
		terr.TuiWrongOperationError("power", "array")
	match var.type:
		case al.DT_TYPES.INT:
			if type(added) is al.Variable:
				if added.type is al.DT_TYPES.INT:
					var.vl = var.get_value() ** added.get_value()
				else:
					terr.TuiWrongTypeError("int", added.type.to_python_type().__class__.__name__).trigger()
			else:
				if added.isdigit():
					var.vl = var.get_value() ** int(added)
				else:
					terr.TuiWrongTypeError("int").trigger()
		case al.DT_TYPES.FLT:
			if type(added) is al.Variable:
				if added.isdigit() or added.replace('.', '', 1).isdigit():
					var.vl = var.get_value() ** float(added.get_value())
				else:
					terr.TuiWrongTypeError("flt", added.type.to_python_type().__class__.__name__).trigger()
			else:
				if added.isdigit() or added.replace('.', '', 1).isdigit():
					var.vl = var.get_value() ** float(added)
				else:
					terr.TuiWrongTypeError("flt").trigger()
		case al.DT_TYPES.STR:
			terr.TuiWrongOperationError("power", "str")

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
		case 'list':
			print("dp, dpl, loop, new, set, stt, end, clr, del, exec, add, sub, mu, div, pow, help, fun, ret, vr, call","enable_eq","disable_eq")
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

#TODO consider merging these two commands below
def enable_err_quit_f(args):
	ev._ERR_QUIT = True

def disable_err_quit_f(args):
	ev._ERR_QUIT = False
