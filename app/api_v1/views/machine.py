from flask import Blueprint, make_response, current_app, request
from app.api_v1.MachineManager.MachineManager import MachineManager
from app.api_v1.debug_info import generate_mock_machine
machine_bp = Blueprint("/api/v1", __name__, url_prefix="/api/v1")

@machine_bp.route("/status", methods=["GET"])
def status():
    """See general information of device (uptime, applications running, name)"""      
    payload = MachineManager.get_all_machines()     
       
    return make_response(payload, 200)

@machine_bp.route("/status-debug/<int:count>", methods=["GET"])
def status_debug(count):
    """test endpoint to help design frontend"""      
        
    return make_response({'data': generate_mock_machine(count)}, 200) 

@machine_bp.route("/running-services/<int:id>", methods=["GET"])
def running_services(id):
    """See what applications are running"""
    services = MachineManager.get_running_services(id)

    return make_response({"result": services}, 200)

# add a machine
@machine_bp.route("/add-machine", methods=["POST"])
def add_machine():

    data = request.get_json()

    machine_addr = data["addr"]
    machine_port = data["port"]
    machine_user = data["user"]
    new_machine = MachineManager.add_machine(machine_addr, machine_port, machine_user, current_app.config["KEY_PATH"])
    
    return make_response({"created": new_machine}, 201)


