import paramiko
from sqlmodel import Session, select, delete
# from sqlalchemy import select, delete
# from app.models import db, Machine, Project
from app.models_fast.machine import Machine
# from app.serializer import MachineSchema, ProjectSchema
from app.core.agent_manager.manager import install_agent
from app.core.agent_manager.agent_manager import AgentManager
from app.core.os_platforms.windows import WindowsOS
from app.core.os_platforms.linux import LinuxOS
from app.core.os_platforms.base import BaseOS
from app.core.errors import (MachineConnectionError, UnsupportedMachineOS, MachineAlreadyExists, 
                             MachineDoesNotExist, MissingProjectFields, ProjectDoesNotExist)
from app.features.vscode.command import launch_vscode
from app.features.tailscale_manager.tailscale_manager import TailscaleManager
import requests
OS_HANDLERS = {
        "windows" : WindowsOS(),
        "linux" : LinuxOS()
}


# https://www.geeksforgeeks.org/python/context-manager-in-python/
class SSHClientContextManager:
    def __init__(self, address, port, username, keypath):
        self.address = address
        self.port = port
        self.keypath = keypath
        self.username = username

    def __enter__(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(hostname=self.address, port=self.port,  username=self.username, key_filename=self.keypath)
        return self
    
    def execute(self, command):
        _, stdout, stderr = self.client.exec_command(command)

        cmd_status = stdout.channel.recv_exit_status()

        if cmd_status != 0:
            # print("execute error!", stderr)
            return stderr.read().decode().strip()
        return stdout.read().decode().strip()
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.client.close()

class MachineManager:
    @staticmethod
    async def check_connections(session: Session, key_path: str):
        """Check what machines are online/offline then updates database"""
        machines = session.exec(select(Machine)).all()
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # attempt to connect to each machine
        for machine in machines:
            try:
                client.connect(machine.address, port=machine.port,  username=machine.user, key_filename=key_path, timeout=5)
                machine.is_online = True
            except:
                machine.is_online = False
            finally:
                session.commit()
                client.close()
                
    # NOTE: unused
    @staticmethod
    def get_all_machines():
        """Return system information for all machines"""    
        machines = db.session.execute(select(Machine)).scalars()
        
        return MachineSchema(many=True).dump(machines)
    
    @staticmethod
    def detect_os(ssh_manager):
        """
        Check for OS using the helper's execute method.
        """
        if "Microsoft Windows" in ssh_manager.execute("ver"):
            return "windows"
            
        if ssh_manager.execute("uname") == "Linux":
            return "linux"
            
        return None
    
    @staticmethod
    def add_machine(address, port, username, keypath, session: Session):
        # machine = db.session.execute(select(Machine).where(Machine.address == address and Machine.port == port)).scalar_one_or_none()
        machine = session.exec(select(Machine).where(Machine.address == address and Machine.port == port)).one_or_none()
        if machine:
            raise MachineAlreadyExists
        try:
            with SSHClientContextManager(address=address, port=port, username=username, keypath=keypath) as sshConn:
                os_type = MachineManager.detect_os(sshConn)
    
                if not os_type:
                    raise UnsupportedMachineOS
                         
                os_handler = OS_HANDLERS.get(os_type)
                sys_info = os_handler.get_system_info(sshConn.execute)
                sys_info['os_type'] = os_type
                sys_info['user'] = username
                sys_info['port'] = port
                sys_info['address'] = address
                
                # install tailscale(add to tailnet)
                ts = TailscaleManager(tags=["tag:dashboard-node"])
                sys_info['tailscale_ip'] = ts.add_to_tailnet(ssh_conn=sshConn, os_handler=os_handler, hostname=username)
                # new_machine = MachineSchema().load(data=sys_info, session=db.session)
                new_machine = Machine(**sys_info)

                # install local reporting agent
                AgentManager.install(new_machine)
                # db.session.add(new_machine)
                session.add(new_machine)
                session.commit()
                session.refresh(new_machine)
                # db.session.commit()
                return sys_info
        except TimeoutError:
            raise MachineConnectionError
    
    @staticmethod
    def get_usage(machine_id, session: Session):
        machine = session.exec(select(Machine).where(Machine.id == machine_id)).one_or_none()
        if not machine:
            raise MachineDoesNotExist
        try:
            res = requests.get(f"http://{machine.tailscale_ip.strip()}:8001")
            return res.json()
        except:
            return None

    @staticmethod
    def remove_machine(machine_id, session: Session):
        session.exec(delete(Machine).where(Machine.id == machine_id))
        session.commit()

    # TODO
    @staticmethod
    def restart_machine(machine_id, keypath):
        machine = db.session.execute(select(Machine).where(Machine.id==machine_id)).scalar_one_or_none()

        if not machine:
            raise MachineDoesNotExist
        
        machine_handler = OS_HANDLERS.get(machine.os_type)

        with SSHClientContextManager(machine.address, machine.port, machine.user, keypath) as client:
            # Execute restart command
            machine_handler.restart(client.execute)

    # TODO
    @staticmethod
    def get_running_services(machine_id, keypath, offset=None):
        # return machine info + running apps

        machine = db.session.execute(select(Machine).where(Machine.id== machine_id)).scalar_one_or_none()
        ssh_conn = paramiko.SSHClient()
        ssh_conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_conn.connect(machine.address, port=machine.port,  username=machine.user, key_filename=keypath)
        def runner(cmd):
            return MachineManager._execute(ssh_conn, cmd)
        
        os_handler = OS_HANDLERS.get(machine.os_type)

        return os_handler.get_processes(runner)
        
        # if offset:
        #     cmd = f"""powershell "get-process | Sort-Object CPU -Descending | Select-Object -First 5 -Skip {offset} -Property Name, Id, CPU | ConvertTo-Json" """
        # return MachineManager._execute(ssh_client, cmd)
    
    @staticmethod
    def _execute(client : paramiko.SSHClient, command):
        _, stdout, stderr = client.exec_command(command)

        # Get exit code
        cmd_status = stdout.channel.recv_exit_status()

        if cmd_status != 0:
            # print("execute error!")
            return stderr.read().decode().strip()
        return stdout.read().decode().strip()
    
    @staticmethod
    def open_vscode(machine_id, session: Session):
        """
        open vscode on the client machine connected to the targeted machine
        NOTE: This only works with browser not in VSCode browser
        """
        machine = session.exec(select(Machine).where(Machine.id == machine_id)).one_or_none()
        return launch_vscode(machine.user, machine.address, machine.user, machine.os_type)
    

        




