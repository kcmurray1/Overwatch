from flask.views import MethodView
from app.machine_manager import MachineManager
from app.core.errors import response_template

class ProjectBlueprints(MethodView):
    def get(self):
        blueprints = MachineManager.get_blueprints()

        return response_template(200, "ok", blueprints)