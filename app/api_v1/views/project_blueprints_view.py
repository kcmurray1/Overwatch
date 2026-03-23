from flask.views import MethodView
from app.extensions import docker_orchestrator
from app.core.errors import response_template

class ProjectBlueprints(MethodView):
    def get(self):
        blueprints = docker_orchestrator.get_blueprints()
        return response_template(200, "ok", blueprints)