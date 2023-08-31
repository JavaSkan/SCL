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
		print("Args don't match")

def displayl_f(args):
	try:
		display_f(args)
		print()
	except IndexError:
		print("Args don't match")


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
		raise terr.TuiInvalidNameError(args[0])
	if args[0] in al.DT_TYPES.TYPES:
		if args[0] == "str":
			al.Variable(args[0],args[1],ul.var_ref(" ".join(args[2:])))
		else:
			al.Variable(args[0],args[1],ul.var_ref("".join(args[2:])))
	elif args[0] == "arr":
		al.Array(args[1],ul.parse_arr(args[2]))
	else:
		print(f"Unknown type {args[0]}")


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
			print("Unknown End Error")
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
			print("Incorrect file extension")
	else:
		print("There is not such file")

def add_f(args):
	var = ev.get_from_id(args[0])
	try:
		match al.DT_TYPES.TYPES[var.type]:
			case al.DT_TYPES.INT:
				var.vl = str(var.get_value() + int(ul.var_ref(args[1])))
			case al.DT_TYPES.FLT:
				var.vl = str(var.get_value() + float(ul.var_ref(args[1])))
			case _:
				print("The variable type is not a number")
	except ValueError:
		print("Types are mismatching")

def sub_f(args):
	var = ev.get_from_id(args[0])
	if al.DT_TYPES.TYPES[var.type] in al.DT_TYPES.NUMBERS:
		match al.DT_TYPES.TYPES[var.type]:
			case al.DT_TYPES.INT:
				var.vl = str(var.get_value() - int(ul.var_ref(args[1])))
			case al.DT_TYPES.FLT:
				var.vl = str(var.get_value() - float(ul.var_ref(args[1])))
	else:
		print("The variable type is not a number")

def mul_f(args):
	var = ev.get_from_id(args[0])
	if al.DT_TYPES.TYPES[var.type] in al.DT_TYPES.NUMBERS:
		match al.DT_TYPES.TYPES[var.type]:
			case al.DT_TYPES.INT:
				var.vl = str(var.get_value() * int(ul.var_ref(args[1])))
			case al.DT_TYPES.FLT:
				var.vl = str(var.get_value() * float(ul.var_ref(args[1])))
	else:
		print("The variable type is not a number")

def div_f(args):
	var = ev.get_from_id(args[0])
	if al.DT_TYPES.TYPES[var.type] in al.DT_TYPES.NUMBERS:
		match al.DT_TYPES.TYPES[var.type]:
			case al.DT_TYPES.INT:
				var.vl = str(var.get_value() / int(ul.var_ref(args[1])))
			case al.DT_TYPES.FLT:
				var.vl = str(var.get_value() / float(ul.var_ref(args[1])))
	else:
		print("The variable type is not a number")

def pow_f(args):
	var = ev.get_from_id(args[0])
	if al.DT_TYPES.TYPES[var.type] in al.DT_TYPES.NUMBERS:
		match al.DT_TYPES.TYPES[var.type]:
			case al.DT_TYPES.INT:
				var.vl = str(var.get_value() ** int(ul.var_ref(args[1])))
			case al.DT_TYPES.FLT:
				var.vl = str(var.get_value() ** float(ul.var_ref(args[1])))
	else:
		print("The variable type is not a number")

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
		case 'list':
			print("dp, dpl, loop, new, set, stt, end, clr, del, exec, add, sub, mu, div, pow, help, fun, ret, vr, call")
		case _:
			print("Unknown Command, either it does not exist or there is no manual for it")

def fun_f(args):
	if not ul.is_valid_name(args[0]):
		raise terr.TuiInvalidNameError(args[0])

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
		print(f'{args[0]} is not a valid argument for this command')

def call_f(args):
	if (fun := ev.get_from_id(args[0])) == None:
		raise terr.TuiNotFoundError(args[0])
	if type(fun) is not al.Function:
		raise terr.TuiNotCallableError(args[0])
	fun.execute_fun(args[1:])
