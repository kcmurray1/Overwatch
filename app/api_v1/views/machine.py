from flask import Blueprint, make_response, current_app, request
from sqlalchemy import Select
import paramiko
from app.api_v1.MachineManager.MachineManager import MachineManager
from app.models import db, Machine
from app.serializer import MachineSchema, WatchlistSchema

machine_bp = Blueprint("/api/v1", __name__, url_prefix="/api/v1")

@machine_bp.route("/status", methods=["GET"])
def status():
    """See general information of device (uptime, applications running, name)"""

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        # read from db
        machines = db.session.execute(Select(Machine).where(Machine.id==2)).scalars()

   
        for machine in machines:
       
            client.connect(machine.addr, port=machine.port,  username=machine.user, key_filename=current_app.config["KEY_PATH"])
            stats = MachineManager.get_status(client)
            print(stats)

        client.close()
        return make_response({"status": stats}, 200)
    except Exception as e:
        return make_response({"error": f"Unable to connect: {str(e)}"}, 500)



# add a machine
@machine_bp.route("/add-machine", methods=["POST"])
def add_machine():

    data = request.get_json()


    machine_addr = data["addr"]
    machine_port = data["port"]
    machine_user = data["user"]
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    client.connect(machine_addr, port=machine_port,  username=machine_user, key_filename=current_app.config["KEY_PATH"])
    
    print(data)
    # add to database upon successful connection
    new_machine = MachineSchema().load(data=data, session=db.session)

    db.session.add(new_machine)
    db.session.commit()

    client.close()

    
    return make_response({"created": MachineSchema().dump(new_machine)}, 201)
# except Exception as e:
    #     return make_response({"error": f"{str(e)}"}, 500)



