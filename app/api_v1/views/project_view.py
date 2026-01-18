from flask.views import MethodView
from flask import make_response, current_app, request
from app.machine_manager import MachineManager
from app.api_v1.debug_info import generate_mock_machine
from app.core.errors import APIError, response_template

class ProjectCollection(MethodView):

    def get(self):
        pass
    
    def post(self):
        pass


class ProjectRecord(MethodView):
    def delete(id):
        pass