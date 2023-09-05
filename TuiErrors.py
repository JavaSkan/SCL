import env

class TuiError:

    def __init__(self,msg):
        self.err_msg = msg

    def trigger(self):
        print(f"\033[0;31mERROR: {self.err_msg}\033[0m")
        if env._ERR_QUIT:
            quit()

#TODO create a TuiUnknownCommand error
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
        self.msg = "Arguments don't match: " + (f"provided {nap - nan} extra argument(s)" if nap > nan \
                                                  else
                                              f"missing {nan - nap} arguments")
        super().__init__(self.msg)

class TuiNotFoundError(TuiError):
    """
    id: id of the variable
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