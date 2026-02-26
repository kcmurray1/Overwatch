import paramiko
from sqlalchemy import select, delete
from app.models import db, Machine, Project
from app.serializer import MachineSchema, ProjectSchema
from app.core.os_platforms.windows import WindowsOS
from app.core.os_platforms.linux import LinuxOS
from app.core.os_platforms.base import BaseOS
from app.core.errors import (MachineConnectionError, UnsupportedMachineOS, MachineAlreadyExists, 
                             MachineDoesNotExist, MissingProjectFields, ProjectDoesNotExist)
from app.features.vscode.command import launch_vscode
from app.features.tailscale_manager.tailscale_manager import TailscaleManager
from app.features.docker_manager.blueprints.base_blueprint import BLUEPRINT_REGISTRY, BLUEPRINT_STRUCTURES
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
            print("execute error!", stderr)
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
    def add_machine(address, port, username, keypath):
        machine = db.session.execute(select(Machine).where(Machine.address == address and Machine.port == port)).scalar_one_or_none()
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
                
                print("adding to database...", flush=True)
                new_machine = MachineSchema().load(data=sys_info, session=db.session)
      
                db.session.add(new_machine)
                db.session.commit()
                return sys_info
        except TimeoutError:
            raise MachineConnectionError

        
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
    def get_projects():
        projects = db.session.execute(select(Project)).scalars()
        return  ProjectSchema(many=True).dump(projects)
    
    # FIXME: maybe return a receipt? FOr example to let user know what was shutdown and what wasn't in case of failure
    def stop_project(id):
        project = db.session.execute(select(Project).where(Project.id == id)).scalar_one_or_none()
        if not project:
            return ProjectDoesNotExist
        
        recipe = BLUEPRINT_REGISTRY[project.strategy_type]
        
        machine_objects = Project.hydrate_machines(project.deployment_metadata['machines'])
        result = recipe().stop(machine_objects)
        project.is_running = False
        db.session.commit()
        return {}
    
    def get_project(id):
        project = db.session.execute(select(Project).where(Project.id == id)).scalar_one_or_none()
        if not project:
            raise ProjectDoesNotExist
        return ProjectSchema().dump(project)
    
    def remove_project(id):
        project = db.session.execute(select(Project).where(Project.id == id)).scalar_one_or_none()
        if not project:
            return ProjectDoesNotExist
        
        recipe = BLUEPRINT_REGISTRY[project.strategy_type]
        
        machine_objects = Project.hydrate_machines(project.deployment_metadata['machines'])
        result = recipe().remove(machine_objects)
        db.session.execute(delete(Project).where(Project.id == id))
        db.session.commit()
        return {}

    @staticmethod
    def add_project(env, machines, images, recipe, name):
        # a project can not be added if no recipe or machine is selected
        if not recipe or not machines:
            raise MissingProjectFields(message="Missing recipe and machine(s) selection")
        
        recipe_obj = BLUEPRINT_REGISTRY[recipe]
     
        machines_cleaned = Project.hydrate_machines(machines)
        print("cleaned machines before adding project")
 
        result = recipe_obj().create(name, env, images, machines_cleaned)

        new_project = Project(
            name=name,
            strategy_type=recipe,
        )  
        db.session.add(new_project)
        db.session.flush()
        new_project.config = {"env": env, "machines": machines, "images": images}
        print("saving..", result)
        new_project.deployment_metadata = {"machines" : result}
        
        db.session.commit()
        return ProjectSchema().dump(new_project)
    
    def start_project(id):
        # get project
        project = db.session.execute(select(Project).where(Project.id == id)).scalar_one_or_none()

        if not project:
            raise ProjectDoesNotExist
        
        blueprint_obj = BLUEPRINT_REGISTRY.get(project.strategy_type)
        if not blueprint_obj:
            # FIXME: check if invalid blueprint key
            pass
        updated_machines = Project.hydrate_machines(project.deployment_metadata['machines'])
        blueprint_obj().start(updated_machines)

        project.is_running = True
        db.session.commit()
    

    def get_blueprints():
        return [BLUEPRINT_STRUCTURES[k] for k in BLUEPRINT_STRUCTURES]

        




