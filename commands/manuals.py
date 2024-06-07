DP =      '>>> Displays something on the screen\n'+ \
          'Syntax: dp <string of characters>\n' + \
          'NOTE:\n'+\
          ' -compatible with variable referencing anywhere\n' + \
          ' -to avoid problems with parsing, if you want to display a string of chars containing } ] ) or >, wrap it in a string expression like:\n' + \
          '"dpl Hello World :<)>" or you can do <dpl Hello World :)>'

DPL =     '>>> Displays something on the screen (like cmd dp) but with an additional end-line\n'+ \
          'Syntax: dpl <string of characters>\n' + \
          'NOTE:\n'+\
          ' -compatible with variable referencing'

LOOP    = '>>> Repeats a set of instructions\n' + \
          'Syntax: loop <value> {body}\n' + \
          'NOTE:\n'+\
          ' -compatible with variable referencing (at <value> argument)\n' + \
          ' -when an integer is given as <value>, the loop acts like a for loop\n' + \
          ' -when a boolean is given as <value>, the loop acts like a while loop'

NEW     = '>>> Creates a new variable\n' + \
          'Syntax: new <kind> <type> <name> <initial_value>\n' + \
          'Kinds are: mut(mutable) const(constant) temp(temporary)' + \
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
          'Syntax: end 0|1|int true|false\n' + \
          '0 for success and 1 for failure,or custom status code, should be an integer\n' + \
          'If second argument is true then a msg with appear, if false nothing will show\n'+\
          'NOTE:\n'+\
          ' -compatible with variable referencing with both arguments'

CLR     = '>>> Clears the environment (Allocations)\n' + \
          'Syntax: clr'

DEL     = '>>> Deletes a variable\n' + \
          'Syntax: del <name>'

EXEC    = '>>> Executes SCl script\n' + \
          'Syntax: exec <file_name_with_extension>'+ \
          'NOTE:\n' + \
          ' -compatible with variable referencing (at <file_name_with_extension> argument)' + \
          ' -<file_name_with_extension> should be a string literal'

OPERTS  = '>>> Performs the wanted operation\n' + \
          'Syntax: add|sub|mul|div|pow <name> <value>\n' + \
          'NOTE:\n'+\
          ' -compatible with variable referencing (at <value> argument)'

HELP    = '>>> Helps you with commands, seriously what did you expect ?\n' + \
          'Syntax: help <cmd_name>|list\n' + \
          'Typing "help list" shows you all manuals available'

FUN     = '>>> Defines a function\n' + \
          'Syntax: fun <type> <name> (params) {body}\n' + \
          'params are defined as: <type> <name>\n'+\
          'NOTE:\n'+\
          ' -before calling a function, its value is null (or None). if you want the function to return something use ret function inside its body and then call it to set its value\n' + \
          ' -The function will keep its previous value until recalling it, and variables created in its content will remain after exiting its execution unlike parameters which are deleted\n' + \
          ' -If ret is not called or not found, the function value will be set to a default value to avoid errors, for integers and floats it\'s 0, for booleans it\'s true, and strings it\'s ""\n' + \
          ' -For more information about ret command, type "help ret"'

RET     = '>>> Returns a value in a function context\n' + \
          'Syntax: ret <value>\n'+ \
          'NOTE:\n'+\
          ' -When called, it sets the environment variable "_FUN_RET" to the specified value. It means that when called out of function context, it could set the "global return value" of the program running\n'+\
          ' -compatible with variable referencing (at <value> argument)'

CALL    = '>>> Calls a function\n' + \
          'Syntax: call <name> [argument(s)]\n' + \
          'NOTE:\n' + \
          ' -compatible with variable referencing (at [argument(s)])\n'

READ    = '>>> Reads input from the user\n' + \
          'Syntax: read <destination>\n' + \
          'Where <destination> is the name of the variable in which the input will be stored'

ARR     = '>>> Creates an array\n' + \
          'Syntax: arr new <type> <name> [...]\n'