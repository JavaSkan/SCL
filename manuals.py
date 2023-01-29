DP =      '>>> Displays something on the screen\n'+ \
          'Syntax: dp <string of characters>\n' + \
          'NOTE: compatible with variable referencing'

DPL =     '>>> Displays something on the screen (like cmd dp) but with an additional end-line\n'+ \
          'Syntax: dpl <string of characters>\n' + \
          'NOTE: compatible with variable referencing'

LOOP    = '>>> Repeats a set of instructions\n' + \
          'Syntax: loop <count> {body}\n' + \
          'NOTE: compatible with variable referencing (at <count> field)'

NEW     = '>>> Creates a new variable\n' + \
          'Syntax: new <type> <name> [<initial_value>]\n' + \
          'Types are: int flt and str\n' + \
          'NOTE: compatible with variable referencing (at <initial_value> field)'

SET     = '>>> Modifies the value of a variable\n' + \
          'Syntax: set <name> <new_value>\n' + \
          'NOTE: compatible with variable referencing (at <new_value> field)'

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
          'NOTE: compatible with variable referencing (at <value> field)'

HELP    = '>>> Helps you with commands, seriously what did you expect ?\n' + \
          'Syntax: help <cmd_name>'

