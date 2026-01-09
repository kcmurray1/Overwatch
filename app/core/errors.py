from flask import make_response

def response_template(status, message, data=None):
    return make_response({"message": message, "data": data}, status)

def unexpected_error(error):
    print(f"Unexpected error {str(error)}")
    return response_template(500, "An Internal server error occured")

def handle_api_error(error):
    return response_template(error.status_code, error.message)

def machine_error(machine_error):
    return response_template(machine_error.status_code, machine_error.message)

class APIError(Exception):
    status_code = 400
    message = "API Error"

    def __init__(self, message=None, data=None):
        if message is not None:
            self.message = message
        if data is not None:
            self.data = data

class MachineError(Exception):
    status_code = 500
    message = "A machine error occured"

    def __init__(self, message=None, data=None):
        self.message = message or self.message
        self.data = data

class MachineAlreadyExists(MachineError):
    message = "Machine Already Exists"

class UnsupportedMachineOS(MachineError):
    message = "Unsupported OS" 

class MachineConnectionError(MachineError):
    status_code = 504
    message = "Machine Timeout"