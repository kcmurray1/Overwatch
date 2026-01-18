from .views import machine_view, project_view
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
    "/machines/<int:id>/<any(restart, stop, add_project, openvs):action>",
    view_func=machine_view.MachineAction.as_view('machine_action'),
    methods=["POST"]
)