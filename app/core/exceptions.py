# core/exceptions.py
from typing import Any, Optional


class AppBaseException(Exception):
    """Base exception for all application domain errors."""
    status_code: int = 500
    message: str = "An unexpected error occurred."

    def __init__(
        self, 
        message: Optional[str] = None, 
        status_code: Optional[int] = None, 
        data: Optional[Any] = None
    ):
        if message is not None:
            self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.data = data
        super().__init__(self.message)


# Generic API Errors
class APIError(AppBaseException):
    status_code = 400
    message = "API Error"


# Machine Domain Exceptions
class MachineError(AppBaseException):
    status_code = 500
    message = "A machine error occurred."


class MachineAlreadyExists(MachineError):
    status_code = 409
    message = "Machine already exists."


class MachineDoesNotExist(MachineError):
    status_code = 404
    message = "Machine does not exist."


class UnsupportedMachineOS(MachineError):
    status_code = 400
    message = "Unsupported machine operating system."


class MachineConnectionError(MachineError):
    status_code = 504
    message = "Machine connection timeout or unreachable."


# Project / Container Domain Exceptions
class ProjectError(AppBaseException):
    status_code = 500
    message = "A project error occurred."


class ProjectDoesNotExist(ProjectError):
    status_code = 404
    message = "Project does not exist."


class MissingProjectFields(ProjectError):
    status_code = 400
    message = "Unable to process project due to missing fields."

    def __init__(self, fields: Optional[str] = None, **kwargs):
        msg = f"Unable to process project missing fields: {fields}" if fields else self.message
        super().__init__(message=msg, **kwargs)