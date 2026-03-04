from .views import machine_view, project_view, project_blueprints_view
from flask import Blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api/v2')


api_bp.add_url_rule(
    "/machines",
    view_func=machine_view.MachineCollection.as_view("machine_collection"),
    methods=["GET","POST"]
)
api_bp.add_url_rule(
    "/machines/debug/<int:count>",
    view_func=machine_view.MachineDebug.as_view('machine_collection_debug'),
    methods=["GET"]
)
api_bp.add_url_rule(
    "/machines/<int:id>",
    view_func=machine_view.MachineRecord.as_view('machine_record'),
    methods=["GET","DELETE"]
)
api_bp.add_url_rule(
    "/machines/<int:id>/<any(restart, stop, add_project, openvs, usage):action>",
    view_func=machine_view.MachineAction.as_view('machine_action'),
    methods=["POST", "GET"]
)
api_bp.add_url_rule(
    "/projects",
    view_func=project_view.ProjectCollection.as_view('project-collection'),
    methods=["GET", "POST"]
)
api_bp.add_url_rule(
    "/projects/<int:id>",
    view_func=project_view.ProjectRecord.as_view('project-record'),
    methods=["GET", "DELETE"]
)
api_bp.add_url_rule(
    "projects/<int:id>/<any(stop, start):action>",
    view_func=project_view.ProjectAction.as_view('project_action'),
    methods=["POST"]
)

api_bp.add_url_rule(
    "blueprints", 
    view_func=project_blueprints_view.ProjectBlueprints.as_view('project_blueprints'),
    methods=["GET"]
)