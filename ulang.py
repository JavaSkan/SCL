import funlink as fl
import env as ev

LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def parse(line):
	res = line.split(" ")
	for i in range(0,res.count("")):
		res.pop(res.index(""))
	return res

def gethead(args):
	return args[0]

def getbody(args):
	body = []
	start = False
	for a in args:
		if a.startswith("{"):
			start = True
			body.append(a[1:])
		elif start and a.endswith("}"):
			body.append(a[:len(a)-1])
			return body
		elif start:
			if a == args[len(args)-1]:
				print("Error: } expected; getbody function in ulang.py")
			else:
				body.append(a)

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
	reassembled = " ".join(args)
	ref_id = ""
	i = 0
	while i < len(reassembled):
		if reassembled[i] == "$":
			i += 1 if i < len(reassembled)-1 else 0
			while i < len(reassembled) and reassembled[i] in LETTERS:
				ref_id += reassembled[i]
				i += 1
			reassembled = reassembled.replace(f"${ref_id}",f"{ev.get_value_from_id(ref_id)}")
			ref_id = ""

		i += 1
	return reassembled.split(" ")


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
		print(f"Command {gethead(args)} does not exist")