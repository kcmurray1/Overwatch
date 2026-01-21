from flask.views import MethodView
from flask import make_response, current_app, request
from app.machine_manager import MachineManager
from app.api_v1.debug_info import generate_mock_machine
from app.core.errors import APIError, response_template

class ProjectCollection(MethodView):

    def get(self):
        return response_template(200, "ok",  MachineManager.get_projects())
    
    def post(self):
        result = MachineManager.add_project(request.get_json())
        return response_template(200, "ok", result)


class ProjectRecord(MethodView):

    def get(self, id):
        return MachineManager.get_project(id)
    
    def delete(self, id):
        removed_project = MachineManager.remove_project(id)

        return response_template(200, "removed", removed_project)



class ProjectAction(MethodView):
    def post(self, id, action):
        if action == "stop":
            return MachineManager.stop_project(id)
