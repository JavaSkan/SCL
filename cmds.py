import ulang as ul
import allocable as al
import env as ev

def display_f(args):
	try:
		res = ""
		for arg in args[1:]:
			if arg == args[len(args)-1]:
				res += arg
			else:
				res += arg+" "
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