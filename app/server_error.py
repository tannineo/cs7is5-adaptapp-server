import sys
from enum import Enum, unique, auto

################################################################
# custom server errors
################################################################


# Error codes for all module exceptions
@unique
class ServerErrorCodes(Enum):
    # error code passed is not specified in enum ErrorCodes
    ERR_INCORRECT_ERRCODE = auto()
    ERR_INPUT_ERROR = auto()
    ERR_NO_AUTHORIZATION = auto()


class ServerError(RuntimeError):
    def __init__(self, error_code, message='', *args, **kwargs):
        # Raise a separate exception in case the error code passed isn't
        # specified in the ErrorCodes enum
        if not isinstance(error_code, ServerError):
            msg = 'Error code passed in the error_code param must be of type {0}'
            raise ServerError(ServerErrorCodes.ERR_INCORRECT_ERRCODE, msg,
                              ServerErrorCodes.__class__.__name__)

        # Storing the error code on the exception object
        self.error_code = error_code

        # storing the traceback which provides useful information about where
        # the exception occurred
        self.traceback = sys.exc_info()

        # Prefixing the error code to the exception message
        try:
            msg = '[{0}] {1}'.format(error_code.name,
                                     message.format(*args, **kwargs))
        except (IndexError, KeyError):
            msg = '[{0}] {1}'.format(error_code.name, message)

        super().__init__(msg)
