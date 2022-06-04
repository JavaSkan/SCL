import os
import ulang as ul
import allocable as al
import env as ev

def display_f(args):
	try:
		res = ""
		add = ""
		for arg in args[1:]:
			if type(arg) is str:
				add = arg
			elif type(arg) is list:
				add = " ".join(arg)

			if arg == args[len(args)-1]:
				res += add
			else:
				res += add+" "
		print(res)
	except IndexError:
		print("Args don't match")


def loop_f(args):
	try:
		insts = ul.get_instructions(ul.getbody(args))
		for i in range(int(args[1])):
			for ins in insts:
				ul.execute(ins)
	except IndexError:
		print("Args don't match")


def new_f(args):
	#valid name ?
	try:
		for c in args[2]:
			if c not in ul.LETTERS:
				print("Variable name should be only formed with letters")
				ul.execute("end ")

		if args[1] == "val":
			al.Variable(args[2],args[3])
		elif args[1] == "arr":
			values = ul.get_arr_values(ul.get_arr_body(args))
			al.Array(args[2],values)
	except IndexError:
		print("Args don't match")


def state_f(args):
	print(f"ALLOCATIONS : {ev._VARS}")
	print(f"BOOL_STATE : {ev._BOOL}")

def end_f(args):

	if len(args) == 1:
		print("user end")
	elif args[1] == "0":
		print("ended successfully")
	elif args[1] == "1":
		print("ended with a failure")
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
		ev.get_from_id(args[1]).vl = args[2]
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