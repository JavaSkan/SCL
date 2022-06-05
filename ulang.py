import string

import funlink as fl
import env as ev

LETTERS = string.ascii_letters

def parse(line):
	res = line.split(" ")
	for i in range(0,res.count("")):
		res.pop(res.index(""))
	return res

def gethead(args):
	try:
		return args[0]
	except IndexError:
		return ""

def getbody(args):
	body = []
	inner = []
	start = False
	i = 0
	while i < len(args):
		if type(args[i]) is list:
			return args[i]
		if args[i].startswith("{"):
			if start == True:
				inner = getbody(args[i:])
				i += len(inner)-1
				body.append(inner.copy())
				inner.clear()
			else:
				start = True
				body.append(args[i][1:])
		elif start and args[i].endswith("}"):
			body.append(args[i][:len(args[i])-1])
			return body
		elif start:
			if args[i] == args[len(args)-1]:
				print("Error: } expected; getbody function in ulang.py")
			else:
				body.append(args[i])
		i += 1
	return body

def get_arr_body(args):
	body = []
	start = False
	for a in args:
		if a.startswith("["):
			start = True
			body.append(a)
		elif start and a.endswith("]"):
			body.append(a)
			return body
		elif start:
			if a == args[len(args)-1]:
				print("Error: ] expected; getbody function in ulang.py")
			else:
				body.append(a)

def get_instructions(body):
	insts = []
	temp_inst = []
	for i in range(0,len(body)):
		if body[i] in [";\n",";"]:
			insts.append(temp_inst[:])
			temp_inst.clear()
		elif body[i] != "":
			temp_inst.append(body[i])
	if temp_inst.__len__() > 0:
		insts.append(temp_inst[:])
		temp_inst.clear()

	return insts

def get_arr_values(arr_body):
	assembled = "".join(arr_body)
	assembled = assembled[1:len(assembled)-1]
	assembled = assembled.split(",")
	return assembled

def replace_variable_reference(args):
	result = []
	ref_id = ""
	is_end = False
	i = 0
	x = 0
	for a in args:
		if type(a) is str:
			dlr_count = a.count("$")
			if dlr_count > 0:
				for k in range(dlr_count):
					x = 0
					while i < len(a):
						x = a.index("$")

						try:
							a = a[:x] + a[x + 1:]  # remove the $ sign
						except IndexError:
							is_end = True

						i = 0
						while i < len(a) and a[i] in LETTERS and not is_end:
							ref_id += a[i]
							i += 1

						# if the $ sign is alone then dont replace it just put it as it is
						if ref_id == "":
							result.append("$")
						else:
							result.append(ev.get_value_from_id(ref_id))

						ref_id = ""
					i = 0
					x += 1
			else:
				result.append(a)
		elif type(a) is list:
			a = replace_variable_reference(a)
			result.append(a)

	return result


def execute(inst):
	args = []
	if type(inst) is str:
		args = parse(inst)
	elif type(inst) is list:
		args = inst
	else:
		print("inst is neither list nor str (ulang.py)")

	args = replace_variable_reference(args)
	try:
		fl.cmds[gethead(args)](args)
	except KeyError:
		pass