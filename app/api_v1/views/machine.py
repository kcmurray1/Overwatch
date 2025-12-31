from flask import Blueprint, make_response, current_app
import paramiko
from app.api_v1.MachineManager.MachineManager import MachineManager

machine_bp = Blueprint("/api/v1", __name__, url_prefix="/api/v1")

@machine_bp.route("/status", methods=["GET"])
def status():
    """See general information of device (uptime, applications running, name)"""

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect("host", port=2003,  username="test", key_filename=current_app.config["KEY_PATH"])

        stats = MachineManager.get_status(client)

        client.close()
        return make_response({"status": stats}, 200)
    except Exception as e:
        return make_response({"error": f"Unable to connect: {str(e)}"}, 500)
    