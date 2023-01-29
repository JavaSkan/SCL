DP =      '>>> Displays something on the screen\n'+ \
          'Syntax: dp <string of characters>\n' + \
          'NOTE:\n'+\
          ' -compatible with variable referencing'

DPL =     '>>> Displays something on the screen (like cmd dp) but with an additional end-line\n'+ \
          'Syntax: dpl <string of characters>\n' + \
          'NOTE:\n'+\
          ' -compatible with variable referencing'

LOOP    = '>>> Repeats a set of instructions\n' + \
          'Syntax: loop <count> {body}\n' + \
          'NOTE:\n'+\
          ' -compatible with variable referencing (at <count> field)'

NEW     = '>>> Creates a new variable\n' + \
          'Syntax: new <type> <name> [<initial_value>]\n' + \
          'Types are: int flt and str\n' + \
          'NOTE:\n'+\
          ' -compatible with variable referencing (at <initial_value> field)'

SET     = '>>> Modifies the value of a variable\n' + \
          'Syntax: set <name> <new_value>\n' + \
          'NOTE:\n'+\
          ' -compatible with variable referencing (at <new_value> field)'

STT     = '>>> Shows the environment state\n' + \
          'Syntax: stt'

END     = '>>> Ends the program\n' + \
          'Syntax: end [0|1] [1]\n' + \
          '0 for success and 1 for failure, nothing for used end\n' + \
          'If second argument is 1 then a msg with appear otherwise nothing will show'

CLR     = '>>> Clears the environment\n' + \
          'Syntax: clr'

DEL     = '>>> Deletes a variable\n' + \
          'Syntax: del <name>'

EXEC    = '>>> Executes TUI script\n' + \
          'Syntax: exec <file_name_with_extension>'

OPERTS  = '>>> Performs the wanted operation\n' + \
          'Syntax: add|sub|mul|div|pow <name> <value>\n' + \
          'NOTE:\n'+\
          ' -compatible with variable referencing (at <value> field)'

HELP    = '>>> Helps you with commands, seriously what did you expect ?\n' + \
          'Syntax: help <cmd_name>'

FUN     = '>>> Defines or calls a function\n' + \
          'Syntax: fun <name> [{body}]\n' + \
          'If {body} is mentioned then fun command defines a function, if not then it will call the function with name <name>\n' + \
          'NOTE:\n'+\
          ' -before calling a function, its value is null (or None). if you want the function to return something use ret function inside its body and then call it to set its value\n' + \
          ' -The function will keep its previous value until recalling it, and variable created in its content will remain after exiting its execution\n' + \
          ' -For more information about ret command, type "help ret"'

RET     = '>>> Returns a value in a function context\n' + \
          'Syntax: ret <value>\n'+ \
          'NOTE:\n'+\
          ' -When called, it sets the environment variable "_FUN_RET" to the specified value. It means that when called out of function context, it could set the "global return value" of the program running\n'+\
          ' -compatible with variable referencing (at <value> field)'

