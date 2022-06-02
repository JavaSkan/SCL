import ulang as ul
import allocable as al
import env as ev

def display_f(args):
	res = ""
	for arg in args[1:]:
		if arg.startswith("$"):
			val = ev.get_value_from_id(arg[1:])
			res += val if val != None else arg
		elif arg == args[len(args)-1]:
			res += arg
		else:
			res += arg+" "						
	print(res)

def loop_f(args):
	insts = ul.get_instructions(ul.getbody(args))
	for i in range(int(args[1])):
		for ins in insts:
			ul.execute(ins)

def new_f(args):
	if args[1] == "val":
		al.Variable(args[2],args[3])
	elif args[1] == "arr":
		values = ul.get_arr_values(ul.get_arr_body(args))
		al.Array(args[2],values)

def state_f(args):
	print(ev._VARS)

def end_f(args):
	quit()