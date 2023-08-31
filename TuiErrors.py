class TuiFunArgsMismatchError(Exception):
    """
    nan: number of arguments needed
    nap: number of arguments provided
    This Error is raised when there is an argument mismatch using functions
    """
    def __init__(self,nan:int,nap:int) -> None:
        self.msg = "Arguments don't match: " + (f"provided {nap - nan} extra argument(s)" if nap > nan \
                                                  else
                                              f"missing {nan - nap} arguments")
        super().__init__(self.msg)

class TuiNotFoundError(Exception):
    """
    id: id of the variable
    This Error is raised when trying to interact with a variable that isn't existing
    """
    def __init__(self,id):
        self.msg = f"Element '{id}' not found"
        super().__init__(self.msg)

class TuiNotCallableError(Exception):
    def __init__(self,id):
        self.msg = f"Element '{id}' cannot be called"
        super().__init__(self.msg)

class TuiInvalidNameError(Exception):
    """
    This Error is raised when naming a variable incorrectly
    """
    def __init__(self,id):
        self.msg = f"'{id}' is not a valid name"
        super().__init__(self.msg)