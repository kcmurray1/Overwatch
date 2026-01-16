from flask import Blueprint, make_response, current_app, request
from app.machine_manager import MachineManager
from app.api_v1.debug_info import generate_mock_machine
from app.core.errors import APIError, response_template

machine_bp = Blueprint("/api/v1", __name__, url_prefix="/api/v1")

@machine_bp.route("/status", methods=["GET"])
def status():
    """See general information of device (uptime, applications running, name)"""      
    payload = MachineManager.get_all_machines()     

    return response_template(status=200, message="ok", data=payload)   

@machine_bp.route("/status-debug/<int:count>", methods=["GET"])
def status_debug(count):
    """test endpoint to help design frontend"""      
        
    return make_response({'data': generate_mock_machine(count)}, 200) 

@machine_bp.route("/running-services/<int:id>", methods=["GET"])
def running_services(id):
    """See what applications are running"""
    services = MachineManager.get_running_services(id)

    return make_response({"result": services}, 200)

@machine_bp.route("/add-machine", methods=["POST"])
def add_machine():
    data = request.get_json()
    print("adding machine", data)
    try:
        machine_addr = data["address"]
        machine_port = data["port"]
        machine_user = data["username"]
    except KeyError:
        raise APIError("Invalid Machine details")
    new_machine = MachineManager.add_machine(machine_addr, machine_port, machine_user, current_app.config["KEY_PATH"])
    return response_template(status=201, message="created", data=new_machine)

@machine_bp.route("/machines/<int:id>", methods=["GET","DELETE"])
def machine_record(id):

    #FIXME: check if id is valid
    if request.method == "GET":
        # all running processes and usage
        # maybe history of uptime?
        # signed in users
        pass
    if request.method == "DELETE":
        MachineManager.remove_machine(id)
    
    return make_response({"result": "ok"}, 200)


@machine_bp.route("/machines/<int:id>/openvs", methods=["GET"])
def open_vscode(id):
    URI = MachineManager.open_vscode(id)

    return response_template(status=200, message="ok", data={"link" : URI})

@machine_bp.route("/machines/<int:id>/restart", methods=["POST"])
def restart_machine(id):

    MachineManager.restart_machine(id)

    return response_template(status=200, message="restarting..")
