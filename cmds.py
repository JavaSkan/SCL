import funlink as fl
import ulang as ul

def print_f(args):
	res = ""
	for arg in args[1:]:
		if arg == args[len(args)-1]:
			res += arg
		else:
			res += arg+" "						
	print(res)

def loop_f(args):
	insts = ul.get_instructions(ul.getbody(args))
	for i in range(int(args[1])):
		for ins in insts:
			ul.execute(ins)