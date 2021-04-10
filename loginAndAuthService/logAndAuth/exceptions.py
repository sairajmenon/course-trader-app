# define Python user-defined exceptions
class Error(Exception):
    """Base class for other exceptions"""
    pass


class UserNameValidationError(Error):
    """Raised when the input value is too small"""
    pass

class EmailValidationError(Error):
    """Raised when the input value is too small"""
    pass

class EmailDoesNotExist(Error):
    """Raised when the input value is too small"""
    pass

class EmailAndPasswordDoNotMatch(Error):
    """Raised when the input value is too large"""
    pass