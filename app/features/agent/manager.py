import paramiko
import os
from dotenv import load_dotenv
from app.models import Machine

IGNORED_PATTERNS = {
    "__pycache__",
    ".venv",
    "venv",
    "env",
    ".git",
    ".idea",
    ".vscode",
    ".pytest_cache",
    "agent.pid",
    ".env"
}

IGNORED_EXTENSIONS = {".pyc", ".pyo", ".pyd", ".log"}

class AgentManager:
    
    @staticmethod
    def _sftp_upload_dir(sftp: paramiko.SFTPClient, local_path: str, remote_path: str):
        """
        Recursively uploads a local directory tree to a remote destination via SFTP.
        """
        # Normalize paths for platform independence
        remote_path = remote_path.replace("\\", "/")
        
        try:
            sftp.mkdir(remote_path)
        except IOError:
            pass  # Remote directory already exists

        for item in os.listdir(local_path):
            if item in IGNORED_PATTERNS:
                continue
            if any(item.endswith(ext) for ext in IGNORED_EXTENSIONS):
                continue
            
            local_item = os.path.join(local_path, item)
            remote_item = f"{remote_path}/{item}"

            if os.path.isdir(local_item):
                AgentManager._sftp_upload_dir(sftp, local_item, remote_item)
            else:
                print(f"Uploading: {item} -> {remote_item}")
                sftp.put(local_item, remote_item)
                
    @staticmethod
    def get_installation_info(os_type, user):
        if os_type == "windows":
            return (
                f'C:/overwatch-agent',
                'setup.ps1'
            )
        elif os_type == "linux":
            return (
                f"/home/{user}/overwatch-agent",
                'setup.sh'
            )
        

    @staticmethod
    def install(machine_model: Machine):
        """
        Install local hardware reporting agent to target machine.
        NOTE: Linux Machines require manual run of setup.sh to approve installation of dependencies.
        """
        load_dotenv()

        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(
            hostname=machine_model.address,
            port=machine_model.port,
            username=machine_model.user,
            key_filename=os.environ.get("KEY_PATH"),
        )

        install_dir, setup_script = AgentManager.get_installation_info(
            machine_model.os_type, machine_model.user
        )

        # Point to the new root node-agent directory
        local_dir = os.path.join(os.getcwd(), "node-agent")

        with client.open_sftp() as sftp:
            print(f"Deploying node-agent to remote path: {install_dir}")
            AgentManager._sftp_upload_dir(sftp, local_dir, install_dir)
            print("SFTP upload complete!")

            if machine_model.os_type == "windows":
                # Start agent or execute setup script on Windows
                script_path = f"{install_dir}/{setup_script}".replace("/", "\\")
                cmd = f'powershell -ExecutionPolicy Bypass -File "{script_path}"'
                
                stdin, stdout, stderr = client.exec_command(cmd)
                print("Powershell Output:", stdout.read().decode())
                print("Powershell Errors:", stderr.read().decode())

        client.close()
        
    @staticmethod
    def update():
        pass
    