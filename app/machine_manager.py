import paramiko
from sqlalchemy import select, delete
from app.models import db, Machine
from app.serializer import MachineSchema
from app.core.os_platforms.windows import WindowsOS
from app.core.os_platforms.linux import LinuxOS
from app.core.os_platforms.base import BaseOS
from app.core.errors import MachineConnectionError, UnsupportedMachineOS, MachineAlreadyExists, MachineDoesNotExist
from app.features.vscode.command import launch_vscode
from app.features.docker_manager.docker_manager import DockerManager
from app.features.docker_manager.strategies.base import STRATEGY_REGISTRY
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

        # Get exit code
        cmd_status = stdout.channel.recv_exit_status()

        if cmd_status != 0:
            print("execute error!")
            return stderr.read().decode().strip()
        return stdout.read().decode().strip()
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.client.close()

class MachineManager:
    @staticmethod
    def check_connections(app):
        """Check what machines are online/offline then updates database"""
        with app.app_context():
            machines = db.session.execute(select(Machine)).scalars()
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # attempt to connect to each machine
            for machine in machines:
                print("attempting connection to", machine.address)
                try:
                    client.connect(machine.address, port=machine.port,  username=machine.user, key_filename=app.config["KEY_PATH"], timeout=5)
                    machine.is_online = True
                except:
                    machine.is_online = False
                finally:
                    db.session.commit()
                    client.close()

    @staticmethod
    def get_all_machines():
        """Return system information for all machines"""     
        print(STRATEGY_REGISTRY)
        machines = db.session.execute(select(Machine)).scalars()
        
        return MachineSchema(many=True).dump(machines)

    @staticmethod
    def get_system_info(ssh_conn, os_handler : BaseOS):
        def runner(cmd):
            return MachineManager._execute(ssh_conn, cmd)
        
        return os_handler.get_system_info(runner)

    @staticmethod
    def detect_os(ssh_conn : paramiko.SSHClient):
        """Run version command for respective OS to determine what OS the connect machine uses"""
        _, stdout, _ = ssh_conn.exec_command("ver")
        if stdout.channel.recv_exit_status() == 0:
            return "windows"
        _, stdout, _ = ssh_conn.exec_command("uname")
        if stdout.channel.recv_exit_status() == 0:
            return "linux"
        
        # machine is not using supported OS
        return None
    
    @staticmethod 
    def add_machine(address, port, username, keypath):
        # check if machine with address and port already exists
        machine = db.session.execute(select(Machine).where(Machine.address == address and Machine.port == port)).scalar_one_or_none()
        if machine:
            raise MachineAlreadyExists
        try:
        
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            # verify connection to machine
            client.connect(address, port=port,  username=username, key_filename=keypath)
            
            # figure out basic static information (cpu, os, os_type[windows or not], )
            os_type = MachineManager.detect_os(client)

            if not os_type:
                raise UnsupportedMachineOS
            
            os_handler = OS_HANDLERS.get(os_type)

            sys_info = MachineManager.get_system_info(ssh_conn=client, os_handler=os_handler)
            sys_info['os_type'] = os_type
            sys_info['user'] = username
            sys_info['port'] = port
            sys_info['address'] = address
            # add to database upon successful connection
            new_machine = MachineSchema().load(data=sys_info, session=db.session)

            
            db.session.add(new_machine)
            db.session.commit()
            return sys_info
        except TimeoutError:
            raise MachineConnectionError
        finally:
            client.close() 
    @staticmethod
    def remove_machine(machine_id):
        db.session.execute(delete(Machine).where(Machine.id == machine_id))
        db.session.commit()

    @staticmethod
    def restart_machine(machine_id, keypath):
        machine = db.session.execute(select(Machine).where(Machine.id==machine_id)).scalar_one_or_none()

        if not machine:
            raise MachineDoesNotExist
        
        machine_handler = OS_HANDLERS.get(machine.os_type)

        with SSHClientContextManager(machine.address, machine.port, machine.user, keypath) as client:
            # Execute restart command
            machine_handler.restart(client.execute)


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
            print("execute error!")
            return stderr.read().decode().strip()
        return stdout.read().decode().strip()
    
    @staticmethod
    def open_vscode(machine_id):
        """open vscode on the client machine connected to the targeted machine"""
        machine = db.session.execute(select(Machine).where(Machine.id == machine_id)).scalar_one_or_none()

        return launch_vscode(machine.user, machine.address, machine.user, machine.os_type)
    
    @staticmethod
    def run_project(project_id):
        # get object from database

        strategy = "basic-selenium"
        config = {}

        dm = DockerManager(strategy)
        
        dm.deploy(config)

    @staticmethod
    def stop_project(project_id):

        strat = "basic-selenium"

        config = {}
        dm = DockerManager(strat)
        
        dm.stop(config)

    @staticmethod
    def add_project(data):
        pass


        




