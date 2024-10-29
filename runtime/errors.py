import sys

CURRENT_LINE = ""

def dangerous(note=None):
    def inner(func):
        def wrapper(*args,**kwargs):
            retval = func(*args,**kwargs)
            if isinstance(retval,SCLError):
                retval.trigger(line=CURRENT_LINE,note= note or "")
            else:
                return retval
        return wrapper
    return inner

def quick_err(tag="GENERIC_ERR",msg=""):
    SCLError(msg=msg).trigger(tag=tag)

class SCLError:
    def __init__(self,msg:str):
        self.err_msg = msg

    def trigger(self,line="",note="",tag="SCL-ERR"):
        self.print(line=line,note=note,tag=tag)
        sys.exit(-1)

    def print(self, line="", note="", tag="SCL-ERR"):
        print("\033[0;31m", end="")
        print(f"[{tag}]: {self.err_msg}")
        if line != "":
            print(f"line: '{line}'")
        if note != "":
            print(f"NOTE: {note}")
        print("\033[0m", end="")

class SCLUnknownCommandError(SCLError):
    """
    comm: the command
    Raised when an unknown command is given
    """
    def __init__(self,comm):
        self.msg = f"Unknown Command '{comm}'"
        super().__init__(self.msg)

class SCLArgsMismatchError(SCLError):
    """
    Raised when arguments are mismatching during a command call
    """
    def __init__(self,extra=""):
        self.msg = "Args don't match"+": "+extra
        super().__init__(self.msg)

class SCLFunArgsMismatchError(SCLError):
    """
    nan: number of arguments needed
    nap: number of arguments provided
    Raised when the number of the function arguments is not equal to the number of the functions' parameters
    """
    def __init__(self,nan:int,nap:int) -> None:
        self.msg = "Function arguments don't match: " + (f"provided {nap - nan} extra argument(s)" if nap > nan
                                                  else
                                              f"missing {nan - nap} arguments")
        super().__init__(self.msg)

class SCLNotFoundError(SCLError):
    """
    identifier: identifier of the object
    Raised when trying to interact with a variable that isn't existing
    """
    def __init__(self,identifier:str) -> None:
        self.msg = f"Element '{identifier}' not found"
        super().__init__(self.msg)

class SCLNotCallableError(SCLError):
    """
    identifier: identifier of the object
    Raised when attempting to call a non-callable object
    """
    def __init__(self,identifier:str) -> None:
        self.msg = f"Element '{identifier}' cannot be called"
        super().__init__(self.msg)

class SCLInvalidIdentError(SCLError):
    """
    identifier: the identifier
    This Error is raised when naming a variable incorrectly
    """
    def __init__(self, identifier: str) -> None:
        self.msg = f"'{identifier}' is not a valid identifier"
        super().__init__(self.msg)

class SCLWrongTypeError(SCLError):
    """
    type_o: original type
    type_p: provided type
    Raised when mismatching types
    """
    def __init__(self,type_o:str,type_p:str="") -> None:
        self.msg = "Wrong Type, "
        if type_p != "":
            self.msg += f"'{type_p}' given instead of '{type_o}'"
        else:
            self.msg += f"value for this operation must be '{type_o}'"
        super().__init__(self.msg)

class SCLWrongReturnTypeError(SCLError):
    """
    to the type of the called function
    funident: function identifier
    ftype: the type of the function
    fprovided: value's type provided
    Raised when attempting to return a type whose type is not corresponding
    """

    def __init__(self, funident:str, ftype:str, fprovided:str):
        super().__init__(f"Function '{funident}' of type '{ftype}' tried to return '{fprovided}'")

class SCLNoReturnValueError(SCLError):
    """
    funident: function identifier
    Raised when attempting to return a value and the function is of type nil
    """
    def __init__(self, funident: str):
        super().__init__(f"Function '{funident}' must return nothing (check the function definition)")

class SCLWrongOperationError(SCLError):
    """
    operation: operation on variable
    type: incompatible type
    Raised when attempting to perform an operation on the wrong type
    """

    def __init__(self, operation: str, type: str):
        self.msg = f"Type '{type}' does not support this operation ({operation})"
        super().__init__(self.msg)

class SCLDivisionByZeroError(SCLError):
    """
    Raised when attempting to divide by zero
    """
    def __init__(self, var_id: str):
        super().__init__(f"Cannot divide '{var_id}' by zero")

class SCLUnknownTypeError(SCLError):
    """
    type_name: the unknown type's name
    Raised when invalid type is given
    """
    def __init__(self, type_name: str):
        super().__init__(f"Invalid type given called '{type_name}'")

class SCLUnknownKindError(SCLError):
    """
    kind_name: the unknown kind's name
    Raised when invalid variable kind is given
    """
    def __init__(self, kind_name: str):
        super().__init__(f"Invalid type given called '{kind_name}'")

class SCLModifyConstantError(SCLError):
    """
    cst_name: the constant name
    Raised when attempting to modify a constant variable
    """
    def __init__(self, cst_name: str):
        super().__init__(f"Attempt of modifying a constant called '{cst_name}'")

class SCLAlreadyExistingError(SCLError):
    """
    identifier: identifier of the object
    allocable: the already existing allocable object
    Raised when attempting to alloc a variable with a taken identifier
    """
    def __init__(self, identifier: str, allocable):
        super().__init__(f"Identifier '{identifier}' is already taken: {allocable.__repr__()}")

class SCLNotExistingPathError(SCLError):
    """
    path: the invalid path
    Raised when a path is invalid
    """
    def __init__(self, path: str):
        super().__init__(f"The path '{path}' is an invalid path or does not exist")

class SCLIsNotAFileError(SCLError):
    """
    path: the path that is not a file
    Raised when attempting to interact with an object other than a file
    """
    def __init__(self, path: str):
        super().__init__(f"This '{path}' is not a file")

class SCLWrongExtensionError(SCLError):
    """
    filename: the name of the file that has the wrong extension
    Raised when attempting to execute an SCL file that doesn't have
    the .scl extension
    """
    def __init__(self, filename: str):
        super().__init__(f"This '{filename}' doesn't have the correct extension '.scl'")

class SCLIndexOutOfBoundError(SCLError):
    """
    index: the given index
    length: the length of the iterable object
    Raised when attempting to access an item in an iterable object
    with an index that is out of bound
    """
    def __init__(self, index: int, length: int):
        super().__init__(f"Index out of bound, index must be in [0..{length}[, got {index}")

class SCLNotIterableError(SCLError):
    """
    identifier: the identifier of the non-iterable object
    Raised when performing iterable operations on a non-iterable object
    """
    def __init__(self, identifier: str):
        super().__init__(f"'{identifier}' is not an iterable object")

class SCLInvalidFormalParameterError(SCLError):
    """
    tokentype_name: the name of the token type provided
    Raised when parsing formal parameters and getting a token other than a declaration
    """
    def __init__(self,tokentype_name: str):
        super().__init__(f"Formal parameter should be a declaration (<type> <name>), got token of type '{tokentype_name}'")

class SCLInvalidEffectiveParameterError(SCLError):
    """
    tokentype_name: the name of the token type provided
    Raised when parsing effective parameters and getting a token other than a literal, a variable reference or an array
    """
    def __init__(self,tokentype_name: str):
        super().__init__(f"Formal parameter should be a literal, a variable reference or an array, got token of type '{tokentype_name}'")

class SCLInvalidBooleanExprError(SCLError):
    """
    bool_exp: the boolean expression
    py_ind:  python indication (python error name/type)
    Raised when providing an invalid boolean expression
    """

    def __init__(self, bool_exp: str, py_ind=""):
        msg = f"Invalid boolean expression provided, please check your expression: '{bool_exp}'"
        msg += "" if py_ind == "" else f", Python indicates: {py_ind}"
        super().__init__(msg)

#TODO Syntax Error