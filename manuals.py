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
          ' -compatible with variable referencing (at <count> argument)'

NEW     = '>>> Creates a new variable\n' + \
          'Syntax: new <type> <name> [<initial_value>]\n' + \
          'Types are: int flt arr and str\n' + \
          'NOTE:\n'+\
          ' -compatible with variable referencing (at <initial_value> argument)'

SET     = '>>> Modifies the value of a variable\n' + \
          'Syntax: set <name> <new_value>\n' + \
          'NOTE:\n'+\
          ' -compatible with variable referencing (at <new_value> argument)'

STT     = '>>> Shows the environment state\n' + \
          'Syntax: stt'

END     = '>>> Ends the program\n' + \
          'Syntax: end [0|1] [1]\n' + \
          '0 for success and 1 for failure, nothing for used end\n' + \
          'If second argument is 1 then a msg with appear otherwise nothing will show\n'+\
          'NOTE:\n'+\
          ' -compatible with variable referencing with both arguments'

CLR     = '>>> Clears the environment\n' + \
          'Syntax: clr'

DEL     = '>>> Deletes a variable\n' + \
          'Syntax: del <name>'

EXEC    = '>>> Executes TUI script\n' + \
          'Syntax: exec <file_name_with_extension>'

OPERTS  = '>>> Performs the wanted operation\n' + \
          'Syntax: add|sub|mul|div|pow <name> <value>\n' + \
          'NOTE:\n'+\
          ' -compatible with variable referencing (at <value> argument)'

HELP    = '>>> Helps you with commands, seriously what did you expect ?\n' + \
          'Syntax: help <cmd_name>|list\n' + \
          'Typing "help list" shows you all manuals available'

FUN     = '>>> Defines a function\n' + \
          'Syntax: fun <name> [(params)] {body}\n' + \
          'params are defined as: <type> <name> [value (optional)]\n'+\
          'params are also compatible with variable referencing (at [value])\n'+\
          'NOTE:\n'+\
          ' -before calling a function, its value is null (or None). if you want the function to return something use ret function inside its body and then call it to set its value\n' + \
          ' -The function will keep its previous value until recalling it, and variables created in its content will remain after exiting its execution unlike parameters which are deleted\n' + \
          ' -For more information about ret command, type "help ret"'

RET     = '>>> Returns a value in a function context\n' + \
          'Syntax: ret <value>\n'+ \
          'NOTE:\n'+\
          ' -When called, it sets the environment variable "_FUN_RET" to the specified value. It means that when called out of function context, it could set the "global return value" of the program running\n'+\
          ' -compatible with variable referencing (at <value> argument)'

VR      = '>>> Changes the default character for variable referencing\n' + \
          'Syntax: vr set|reset [new_character]\n' + \
          '<new_character> should be defined if first argument is "set"\n'+ \
          'By default it\'s "$"'

CALL    = '>>> Calls a function\n' + \
          'Syntax: call <name> [argument(s)]\n' + \
          'NOTE:\n' + \
          ' -compatible with variable referencing (at [argument(s)])\n'

ENABLE_EQ = '>>> Enables Error Quitting\n' + \
            'Error Quitting: Program Ends when an error is triggered\n' + \
            'Syntax: enable_eq'

DISABLE_EQ = '>>> Disables Error Quitting\n' + \
             'Error Quitting: Program Ends when an error is triggered\n' + \
             'Syntax: disable_eq'
