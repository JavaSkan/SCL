import os
import ulang as ul
import allocable as al
import env as ev
import manuals

#TODO fix display commands not supporting arrays
def display_f(args):
	try:
		res = ""
		add = ""
		for arg in args[1:]:
			add = ul.var_ref(arg)
			if arg == args[len(args)-1]:
				res += add
			else:
				res += add+" "
		print(res,end="")
	except IndexError:
		print("Args don't match")

def displayl_f(args):
	try:
		res = ""
		add = ""
		for arg in args[1:]:
			add = ul.var_ref(arg)

			if arg == args[len(args)-1]:
				res += add
			else:
				res += add+" "
		print(res)
	except IndexError:
		print("Args don't match")


def loop_f(args):
	insts = ul.parse_block(args[2])
	for i in range(int(ul.var_ref(args[1]))):
		for ins in insts:
			if type(ins) is str:
				ul.execute(ins)
			else:
				ul.execute_block(ins)


def new_f(args):
	#valid name ?
	if not ul.is_valid_name(args[2]):
		print("Variable name should only be formed with Letters")

	if args[1] in al.DT_TYPES.TYPES:
		if args[1] == "str":
			al.Variable(args[1],args[2],ul.var_ref(" ".join(args[3:])))
		else:
			al.Variable(args[1],args[2],ul.var_ref("".join(args[3:])))
	elif args[1] == "arr":
		al.Array(args[2],ul.parse_arr(args[3]))
	else:
		print(f"Unknown type {args[1]}")


def state_f(args):
	print(f"ALLOCATIONS : {ev._VARS}")
	print(f"BOOL_STATE : {ev._BOOL}")
	print(f"FUNCTION RETURN VALUE : {ev._FUN_RET}")
	print(f"VARIABLE REFERENCING SYMBOL : {ev._VARREF_SYM}")

def end_f(args):
	if len(args) != 1:
		if ul.var_ref(args[1]) == "0":
			if len(args) == 3:
				if ul.var_ref(args[2]) == "1":
					print("ended successfully")
		elif ul.var_ref(args[1]) == "1":
			if len(args) == 3:
				if ul.var_ref(args[2]) == "1":
					print("ended with a failure")
		else:
			print("Unknown End Error")

	ev._VARS.clear()
	quit()

def clear_f(args):
	ev._VARS.clear()

def delete_f(args):
	ev._VARS.pop(ev._VARS.index(ev.get_from_id(args[1])))


def set_f(args):
	ev.get_from_id(args[1]).vl = ul.var_ref(args[2])

def execute_f(args):
	if os.path.exists(args[1]):
		if args[1].endswith(".tui"):
			with open(args[1],"r") as f:
				lines = f.read().split("\n")
				for line in lines:
					ul.execute(line)
		else:
			print("Incorrect file extension")
	else:
		print("There is not such file")

def add_f(args):
	var = ev.get_from_id(args[1])
	try:
		match al.DT_TYPES.TYPES[var.type]:
			case al.DT_TYPES.INT:
				var.vl = str(var.get_value() + int(ul.var_ref(args[2])))
			case al.DT_TYPES.FLT:
				var.vl = str(var.get_value() + float(ul.var_ref(args[2])))
			case _:
				print("The variable type is not a number")
	except ValueError:
		print("Types are mismatching")

def sub_f(args):
	var = ev.get_from_id(args[1])
	if al.DT_TYPES.TYPES[var.type] in al.DT_TYPES.NUMBERS:
		match al.DT_TYPES.TYPES[var.type]:
			case al.DT_TYPES.INT:
				var.vl = str(var.get_value() - int(ul.var_ref(args[2])))
			case al.DT_TYPES.FLT:
				var.vl = str(var.get_value() - float(ul.var_ref(args[2])))
	else:
		print("The variable type is not a number")

def mul_f(args):
	var = ev.get_from_id(args[1])
	if al.DT_TYPES.TYPES[var.type] in al.DT_TYPES.NUMBERS:
		match al.DT_TYPES.TYPES[var.type]:
			case al.DT_TYPES.INT:
				var.vl = str(var.get_value() * int(ul.var_ref(args[2])))
			case al.DT_TYPES.FLT:
				var.vl = str(var.get_value() * float(ul.var_ref(args[2])))
	else:
		print("The variable type is not a number")

def div_f(args):
	var = ev.get_from_id(args[1])
	if al.DT_TYPES.TYPES[var.type] in al.DT_TYPES.NUMBERS:
		match al.DT_TYPES.TYPES[var.type]:
			case al.DT_TYPES.INT:
				var.vl = str(var.get_value() / int(ul.var_ref(args[2])))
			case al.DT_TYPES.FLT:
				var.vl = str(var.get_value() / float(ul.var_ref(args[2])))
	else:
		print("The variable type is not a number")

def pow_f(args):
	var = ev.get_from_id(args[1])
	if al.DT_TYPES.TYPES[var.type] in al.DT_TYPES.NUMBERS:
		match al.DT_TYPES.TYPES[var.type]:
			case al.DT_TYPES.INT:
				var.vl = str(var.get_value() ** int(ul.var_ref(args[2])))
			case al.DT_TYPES.FLT:
				var.vl = str(var.get_value() ** float(ul.var_ref(args[2])))
	else:
		print("The variable type is not a number")

def help_f(args):
	match args[1]:
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
		case 'list':
			print("dp, dpl, loop, new, set, stt, end, clr, del, exec, add, sub, mu, div, pow, help, fun, ret, vr")
		case _:
			print("Unknown Command, either it does not exist or there is no manual for it")

def fun_f(args):
	if not ul.is_valid_name(args[1]):
		print("Function name should only be formed with Letters")
		ul.execute("end")
	if len(args) == 2:
		ev.get_from_id(args[1]).execute_fun()
	elif len(args) == 3:
		al.Function(args[1],ul.parse_block(args[2]))

def ret_f(args):
	ev._FUN_RET = ul.var_ref(args[1])

def vr_f(args):
	if args[1] == 'set':
		ev._VARREF_SYM = args[2]
	elif args[1] == 'reset':
		ev._VARREF_SYM = '$'
	else:
		print(f'{args[1]} is not a valid argument for this command')