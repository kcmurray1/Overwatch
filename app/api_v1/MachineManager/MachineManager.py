import paramiko
import json
from sqlalchemy import Select
from flask import current_app
from app.models import db, Machine
from app.serializer import MachineSchema
from app.api_v1.os_platforms.windows import WindowsOS
from app.api_v1.os_platforms.linux import LinuxOS
from app.api_v1.os_platforms.base import BaseOS

OS_HANDLERS = {
        "windows" : WindowsOS(),
        "linux" : LinuxOS()
}

class MachineManager:
   
    @staticmethod
    def get_all_machines():
        """Return system information for all machines"""
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        machines = db.session.execute(Select(Machine)).scalars()
        
        machine_data = list()

        for machine in machines:
            try:
                machine_info = MachineSchema().dump(machine)
                client.connect(machine.address, port=machine.port,  username=machine.user, key_filename=current_app.config["KEY_PATH"], timeout=5)
                machine_info['is_online'] = True
                #FIXME:check if applications in watchlist are running
            except:
                machine_info['is_online'] = False
            finally:
                client.close()
                machine_data.append(machine_info)  

        return {'machines' : machine_data}

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
        
        return None
    
    @staticmethod 
    def add_machine(address, port, username, keypath):
        try:
        
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            # verify connection to machine
            client.connect(address, port=port,  username=username, key_filename=keypath)
            
            # figure out basic static information (cpu, os, os_type[windows or not], )
            os_type = MachineManager.detect_os(client)

            if not os_type:
                return NotImplementedError
            
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
            client.close()
            return sys_info
        except Exception as e:
            print(f"Error adding machine {str(e)}")
            return e


   
        

    def get_running_services(machine_id, offset=None):
        # return machine info + running apps

        machine = db.session.execute(Select(Machine).where(Machine.id== machine_id)).scalar_one_or_none()
        ssh_conn = paramiko.SSHClient()
        ssh_conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_conn.connect(machine.address, port=machine.port,  username=machine.user, key_filename=current_app.config["KEY_PATH"])
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


