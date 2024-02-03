class TuiError:

    def __init__(self,msg:str):
        self.err_msg = msg

    def trigger(self,line="",note=""):
        print("\033[0;31m",end="")
        if line != "":
            print(f'line: "{line}"')
        print(f"ERROR: {self.err_msg}")
        if note != "":
            print(f"NOTE:{note}")
        print("\033[0m",end="")
        quit()
        # if env._ERR_QUIT:
        #     quit()

class TuiUnknownCommand(TuiError):
    """
    comm: the command
    Raised when an unknown command is given
    """
    def __init__(self,comm):
        self.msg = "Unknown Command"
        super().__init__(self.msg)

class TuiArgsMismatchError(TuiError):
    """
    Raised when arguments are mismatching during a command call
    """
    def __init__(self):
        self.msg = "Args don't match"
        super().__init__(self.msg)

class TuiFunArgsMismatchError(TuiError):
    """
    nan: number of arguments needed
    nap: number of arguments provided
    Raised when there is an argument mismatch using functions
    """
    def __init__(self,nan:int,nap:int) -> None:
        self.msg = "Arguments don't match: " + (f"provided {nap - nan} extra argument(s)" if nap > nan
                                                  else
                                              f"missing {nan - nap} arguments")
        super().__init__(self.msg)

class TuiNotFoundError(TuiError):
    """
    id: id of the allocable
    Raised when trying to interact with a variable that isn't existing
    """
    def __init__(self,id:str) -> None:
        self.msg = f"Element '{id}' not found"
        super().__init__(self.msg)

class TuiNotCallableError(TuiError):
    """
    Raised when attempting to call a non-callable object
    """
    def __init__(self,id:str) -> None:
        self.msg = f"Element '{id}' cannot be called"
        super().__init__(self.msg)

class TuiInvalidNameError(TuiError):
    """
    This Error is raised when naming a variable incorrectly
    """
    def __init__(self,id:str) -> None:
        self.msg = f"'{id}' is not a valid name"
        super().__init__(self.msg)

class TuiWrongTypeError(TuiError):
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

class TuiWrongOperationError(TuiError):
    """
    operation: operation on variable
    type: incompatible type
    Raised when attempting to perform an operation on the wrong type
    """

    def __init__(self,operation:str,type:str):
        self.msg = f"Type '{type}' does not support this operation ({operation})"
        super().__init__(self.msg)

class TuiDivisionByZeroError(TuiError):
    """
    Raised when attempting to divide by zero
    """

    def __init__(self,var_id:str):
        super().__init__(f"Cannot divide '{var_id}' by zero")

class TuiUnknownTypeError(TuiError):
    """
    Raised invalid type is given
    """

    def __init__(self, type_name: str):
        super().__init__(f"Invalid type given called '{type_name}'")