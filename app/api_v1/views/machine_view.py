from flask.views import MethodView
from flask import current_app, request
from app.machine_manager import MachineManager
from app.api_v1.debug_info import generate_mock_machine
from app.core.errors import APIError, response_template



import threading
import requests
# Your main Flask monitor's endpoint to receive updates
CONTROL_PLANE_WEBHOOK = "http://<your-flask-server-ip>/api/container-event"
MACHINE_ID = "node-01"  # Or dynamically pulled from your config

def watch_docker_events():
    import docker
    try:
        client = docker.from_env()  # Automatically picks up unix://var/run/docker.sock
        print("Started watching local Docker events...")
        
        # This loop blocks and waits for events natively from the local socket
        for event in client.events(decode=True):
            print(event)
            # We only care about container status changes (start, die, pause, destroy)
            # if event.get("Type") == "container":
            #     container_id = event.get("id")
            #     action = event.get("Action")
            #     attributes = event.get("Actor", {}).get("Attributes", {})
            #     container_name = attributes.get("name")
                
            #     # Format a lightweight payload for your Flask control plane
            #     payload = {
            #         "machine_id": MACHINE_ID,
            #         "container_id": container_id[:12],
            #         "container_name": container_name,
            #         "status": "running" if action in ["start", "unpause"] else "stopped",
            #         "raw_action": action
            #     }
                
                    
    except Exception as e:
        print(f"Docker event listener crashed: {e}")


class MachineDebug(MethodView):
    def get(self, count):
        return response_template(200, "ok", generate_mock_machine(count)) 

class MachineCollection(MethodView):
    def get(self):
        # thread = threading.Thread(target=watch_docker_events, daemon=True)
        # thread.start()
        payload = MachineManager.get_all_machines()     

        return response_template(status=200, message="ok", data=payload)   

    def post(self):
        data = request.get_json()
        print("adding maching", data)
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
    
    def get(self, id, action):
        if action == "usage":
            data = MachineManager.get_usage(id)
            if not data:
                return response_template(status=404, message='agent not responding')
            return response_template(status=200, message='ok', data=data)
        return response_template(200, "ok")