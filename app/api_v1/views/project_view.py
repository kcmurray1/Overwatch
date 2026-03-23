from flask.views import MethodView
from flask import request
from app.machine_manager import MachineManager
from app.extensions import docker_orchestrator
from app.core.errors import response_template

class ProjectCollection(MethodView):

    def get(self):
        projects = docker_orchestrator.get_projects()
        print(projects)
        return response_template(200, "ok", projects)
    
    def post(self):
        print(request.get_json())
        result = docker_orchestrator.add_project(**request.get_json())

        return response_template(200, "ok", result)


class ProjectRecord(MethodView):

    def get(self, id):
        return docker_orchestrator.get_project(id)
    
    def delete(self, id):
        removed_project = docker_orchestrator.remove_project(id)
        return response_template(200, "OK", removed_project)



class ProjectAction(MethodView):
    def post(self, id, action):
        if action == "stop":
            docker_orchestrator.stop_project(id)
            return response_template(200, "OK")
            
        if action == "start":
            print("starting")

            docker_orchestrator.start_project(id)

            return response_template(200, "OK")
