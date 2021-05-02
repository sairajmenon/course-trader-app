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

class InvalidSessionID(Error):
    pass

class InvalidDeptSelected(Error):
    pass

class InvalidSpecializationSelected(Error):
    pass

class InvalidInterestSelected(Error):
    pass

class InvalidPostMSOptionSelected(Error):
    pass

class CourseNotSpecified(Error):
    pass

class UnableToProvidedRecommendationAtThisTime(Error):
    pass