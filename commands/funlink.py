from commands import cmds

cmds = {"dp":	  cmds.display_f,
		"dpl":	  cmds.displayl_f,
		"loop":   cmds.loop_f,
		"new":    cmds.new_f,
		"set":    cmds.set_f,
		"stt":    cmds.state_f,
		"end":    cmds.end_f,
		"clr":    cmds.clear_f,
		"del":    cmds.delete_f,
		"exec":   cmds.execute_f,
		"add":    cmds.add_f,
		"sub":    cmds.sub_f,
		"mul":	  cmds.mul_f,
		"div": 	  cmds.div_f,
		"pow":	  cmds.pow_f,
		"help":   cmds.help_f,
		"fun":    cmds.fun_f,
		"ret":    cmds.ret_f,
		"call":	  cmds.call_f,
		"read":   cmds.read_f,
		"arr":    cmds.array_f,
		"get":    cmds.get_f,
		"mod":	  cmds.mod_f,
		"len":    cmds.len_f,
		"foreach":cmds.foreach_f,
		"if":     cmds.if_f,
		"":       lambda x: {}
		}