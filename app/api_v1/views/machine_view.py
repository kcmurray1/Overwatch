from flask.views import MethodView
from flask import make_response, current_app, request
from app.machine_manager import MachineManager
from app.api_v1.debug_info import generate_mock_machine
from app.core.errors import APIError, response_template

class MachineDebug(MethodView):
    def get(self, count):
        return response_template(200, "ok", generate_mock_machine(count)) 

class MachineCollection(MethodView):
    def get(self):
        payload = MachineManager.get_all_machines()     

        return response_template(status=200, message="ok", data=payload)   

    def post(self):
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

class MachineRecord(MethodView):
    def get(self, id):
        pass

    def delete(self, id):
        MachineManager.remove_machine(id)
        return response_template(200, "ok")
    
class MachineAction(MethodView):
    def post(self, id, action):
        
        if action == "restart":
            MachineManager.restart_machine(id, current_app.config["KEY_PATH"])
            return response_template(status=200, message="restarting..")
        if action == "openvs":
            URI = MachineManager.open_vscode(id)
            return response_template(status=200, message="ok", data={"link" : URI})


        return response_template(200, "ok")