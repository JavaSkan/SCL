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
	for c in args[2]:
		if c not in ul.LETTERS:
			print("Variable name should be only formed with letters")
			ul.execute("end ")

	if args[1] in al.DT_TYPES.TYPES:
		if args[1] == "str":
			al.Variable(args[1],args[2],ul.var_ref(" ".join(args[3:])))
		else:
			al.Variable(args[1],args[2],ul.var_ref("".join(args[3:])))
	elif args[1] == "arr":
		values = ul.get_arr_values(ul.get_arr_body(args))
		al.Array(args[2],values)
	else:
		print(f"Unknown type {args[1]}")


def state_f(args):
	print(f"ALLOCATIONS : {ev._VARS}")
	print(f"BOOL_STATE : {ev._BOOL}")

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
	try:
		ev._VARS.pop(ev._VARS.index(ev.get_from_id(args[1])))
	except IndexError:
		print("Args don't match")

def set_f(args):
	try:
		ev.get_from_id(args[1]).vl = ul.var_ref(args[2])
	except IndexError:
		print("Args don't match")

def execute_f(args):
	try:
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
	except IndexError:
		print("Args don't match")

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
		case _:
			print("Unknown Command")