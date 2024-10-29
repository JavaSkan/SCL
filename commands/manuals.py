DP      = '''
>>> Displays something on the screen
Syntax: dp <string of characters>
NOTE:
 -compatible with variable referencing anywhere
'''

DPL     = '''
>>> Displays something on the screen (like cmd dp) but with an additional end-line
Syntax: dpl <string of characters>
NOTE:
 -compatible with variable referencing
'''

LOOP    = '''
>>> Repeats a set of instructions
Syntax: loop <value> {body}
NOTE:
 -compatible with variable referencing (at <value> argument)
 -when an integer is given as <value>, the loop acts like a for loop
 -when a boolean is given as <value>, the loop acts like a while loop
'''

NEW     = '''
>>> Creates a new variable
Syntax: new <kind> <type> <name> <initial_value>
Kinds are: mut(mutable) const(constant) temp(temporary)
Types are: int flt arr and str
NOTE:
 -compatible with variable referencing (at <initial_value> argument)
'''

SET     = '''
>>> Modifies the value of a variable
Syntax: set <name> <new_value>
NOTE:
 -compatible with variable referencing (at <new_value> argument)
'''

STT     = '''
>>> Shows the environment state
Syntax: stt
'''

END     = '''
>>> Ends the program
Syntax: end 0|1|int true|false
0 for success and 1 for failure,or custom status code, should be an integer
If second argument is true then a msg with appear, if false nothing will show
NOTE:
 -compatible with variable referencing with both arguments
'''

CLR     = '''
>>> Clears the environment (Allocations)
Syntax: clr
'''

DEL     = '''
>>> Deletes a variable
Syntax: del <name>
'''

EXEC    = '''
>>> Executes SCl script
Syntax: exec <scl_file_path> <cross_environment>
NOTE:
 -compatible with variable referencing (at <file_name_with_extension> and <cross_environment>)
 -<scl_file_path> is a string
 -<cross_environment> is a boolean, when true variables, arrays, aliases etc. will remain
 after the execution in the parent environment, they're deleted otherwise
 -commands in the file must end with a semicolon, content will be ignored after the full command
'''

OPERTS  = '''
>>> Performs the wanted operation
Syntax: add|sub|mul|div|pow <name> <value>
NOTE:
 -compatible with variable referencing (at <value> argument)
'''

HELP    = '''
>>> Helps you with commands, seriously what did you expect ?
Syntax: help <cmd_name>|list
Typing "help list" shows you all manuals available
'''

FUN     = '''
>>> Defines a function
Syntax: fun <type> <name> (params) {body}
params are defined as: <type> <name>
NOTE:
 -before calling a function, its value is null (or None). if you want the function to return something use ret function inside its body and then call it to set its value
 -The function will keep its previous value until recalling it, and variables created in its content will remain after exiting its execution unlike parameters which are deleted
 -If ret is not called or not found, the function value will be set to a default value to avoid errors, for integers and floats it's 0, for booleans it's true, and strings it's ""
 -For more information about ret command, type "help ret"
'''

RET     = '''
>>> Returns a value in a function context
Syntax: ret <value>
NOTE:
 -When called, it sets the environment variable "_FUN_RET" to the specified value. It means that when called out of function context, it could set the "global return value" of the program running
 -compatible with variable referencing (at <value> argument)
'''

CALL    = '''
>>> Calls a function
Syntax: call <name> (argument(s))
NOTE:
 -compatible with variable referencing (at [argument(s)])
'''

READ    = '''
>>> Reads input from the user
Syntax: read <destination>
Where <destination> is the name of the variable in which the input will be stored
'''

ARR     = '''
>>> Creates an array
Syntax: arr new <type> <name> <values>
NOTE:
 -compatible with variable referencing (at <values>)
'''

GET     = '''
>>> Gets a value from an iterable object at a certain index
Syntax: get <iterable> <index> <destination>
NOTE:
 -compatible with variable referencing (at <index>)
'''

MOD     = '''
>>> Modifies a value at a certain index in an iterable object
Syntax: mod <iterable> <index> <new_value>
NOTE:
 -compatible with variable referencing (at <index> and <new_value>)
'''

LEN     = '''
>>> Stores the length of an iterable object in a variable
Syntax: len <iterable> <destination>
'''

FOREACH = '''
>>> Iterate over each element in an iterable object
Syntax: foreach <element> in <iterable> {instructions}
'''

IF      = '''
>>> Executes code in the first body if the given boolean expression evaluates to true. The second
body is executed otherwise.
Syntax: if <boolean expression> {true section} {false section}
NOTE: The boolean expression syntax is : b"<expression>"
use '&' for AND
    '|' for OR
    '!' for NOT
    '=' for equality
    variable referencing (boolean variables)
    and true or false
'''

ALIAS   = '''
>>> Creates or removes aliases for a line of code/command
Syntax: alias create|remove <name> [code]
'''