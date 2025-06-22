"""
Base custom exceptions for the application.

This module defines custom exception classes used throughout
the application for better error handling and messaging.
"""


class ApplicationException(Exception):
    """Base application exception."""

    def __init__(self, message: str, code: int = 500):
        self.message = message
        self.code = code
        super().__init__(self.message)


class NotFoundException(ApplicationException):
    """Exception raised when a requested resource is not found."""

    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, code=404)


class ValidationException(ApplicationException):
    """Exception raised when validation fails."""

    def __init__(self, message: str = "Validation error"):
        super().__init__(message, code=400)


class ConflictException(ApplicationException):
    """Exception raised when there's a conflict with current state."""

    def __init__(self, message: str = "Conflict error"):
        super().__init__(message, code=409)


class UnauthorizedException(ApplicationException):
    """Exception raised when user is not authorized."""

    def __init__(self, message: str = "Unauthorized"):
        super().__init__(message, code=401)


class ForbiddenException(ApplicationException):
    """Exception raised when user is forbidden from accessing resource."""

    def __init__(self, message: str = "Forbidden"):
        super().__init__(message, code=403)
