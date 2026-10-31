import paramiko
from sqlmodel import Session, select, delete
import httpx
import asyncio
import queue
import threading
from fastapi import BackgroundTasks
from app.models import Machine
from app.features.agent.manager import AgentManager
from app.core.os_platforms.windows import WindowsOS
from app.core.os_platforms.linux import LinuxOS
from app.core.os_platforms.base import BaseOS
from app.core.exceptions import (MachineConnectionError, UnsupportedMachineOS, MachineAlreadyExists,
                                 MachineDoesNotExist, MissingProjectFields, ProjectDoesNotExist)
from app.features.vscode.command import launch_vscode
from app.features.tailscale_manager.tailscale_manager import TailscaleManager
from app.config import Settings, get_settings
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
    async def check_agent_connections(session: Session):
        machines = session.exec(select(Machine)).all()

        async with httpx.AsyncClient(timeout=3.0) as client:
            async def ping(machine: Machine):
                host = machine.tailscale_ip or machine.address
                print('checking', host)
                if not host:
                    machine.is_online = False
                    return

                try:
                    response = await client.get(f"http://{host.strip()}:8001/")
                    machine.is_online = (response.status_code == 200)
                except (httpx.RequestError, httpx.HTTPStatusError):
                    try:
                        # check if tailscale is not communicating due to key expiration
                        # if can't connect to machine over ssh then the address changed or the machine is offline, skip tailscale check
                        with SSHClientContextManager(address=machine.address, port=machine.port, username=machine.user, keypath=get_settings().key_path) as sshConn:
                            ts = TailscaleManager(tags=["tag:homelab-core"])
                            # generate new tailscale_ip
                            # NOTE: may want to reconsider design if containers run on the machine's tailscale address
                            # maybe restart the containers with the updated tailscale address or hand out permanent keys instead of ephemeral
                            machine.tailscale_ip = ts.add_to_tailnet(ssh_conn=sshConn, os_handler=OS_HANDLERS.get(machine.os_type), hostname=machine.user)
                    except Exception as ssh_err:
                        print("SSH recover failed", ssh_err)
                        machine.is_online = False
                
                session.add(machine)

            # Fire all checks simultaneously
            if machines:
                await asyncio.gather(*(ping(m) for m in machines))

        session.commit()
                    
    
    @staticmethod
    def detect_os(ssh_manager):
        """
        Check for OS using the helper's execute method.
        """
        print("detecting os...")
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
                print("handling", os_handler)
                sys_info = os_handler.get_system_info(sshConn.execute)
                sys_info['os_type'] = os_type
                sys_info['user'] = username
                sys_info['port'] = port
                sys_info['address'] = address
                
    
                
                # install tailscale(add to tailnet)
                ts = TailscaleManager(tags=["tag:homelab-core"])
                sys_info['tailscale_ip'] = ts.add_to_tailnet(ssh_conn=sshConn, os_handler=os_handler, hostname=username)
                new_machine = Machine(**sys_info)

               
            
                # install local reporting agent
                AgentManager.install(new_machine)
                session.add(new_machine)
                session.commit()
                session.refresh(new_machine)
                # from app.extensions import docker_orchestrator
                from app.features.containers.manager import ContainerManager
                try:
                    # docker_orchestrator.get_info(new_machine, session)
                    ContainerManager.detect_existing_containers(machine_obj=new_machine, session=session)
                except Exception as e:
                    print("could not get docker containers", e)

                return sys_info
        except TimeoutError:
            raise MachineConnectionError
    
    @staticmethod
    def check_ssh_connection(ip, user, port):
        """Verify if machine exists at specified address"""
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname=ip, port=port, username=user, timeout=3) 
            return True
        except Exception as e:
            # print(f'{user}@{ip}', e)
            return False
        finally:
            client.close()

   

    def scan_network(target_machines, session: Session, subnet: str ="10.0.0", num_threads: int =30):
        q = queue.Queue()
        stop_event = threading.Event()
        target_lock = threading.Lock()
        found_machines = set()
        
        for i in range(1, 255):
            q.put(f"{subnet}.{i}")
        
        if not target_machines:
            return
            
        def worker_fn():
            while not q.empty() and not stop_event.is_set():
                try:
                    ip = q.get_nowait()
                except queue.Empty:
                    break
                
                for machine in target_machines:
                    if MachineManager.check_ssh_connection(ip, user=machine["user"], port=machine["port"]):
                        with target_lock:
                            found_machines.add(machine["user"])
                            print(f"{machine["user"]}@{ip}:{machine["port"]}")
                            db_machine = session.exec(select(Machine).where(Machine.id == machine["id"])).one_or_none()
                            if db_machine and (db_machine.address != ip):
                                
                                db_machine.address = ip
                                session.add(db_machine)
                            if len(found_machines) == len(target_machines):
                                stop_event.set()
              
        threads = []
        for _ in range(num_threads):
            t = threading.Thread(target=worker_fn)
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join()
        print(found_machines)
        print("scan complete!")
        session.commit()
    
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
    

    
    @staticmethod
    def deploy_container(machine_ids, data, session:Session, background_tasks: BackgroundTasks):
        from app.features.containers.manager import ContainerManager
        import re
        import json
        machine_objects = session.exec(
            select(Machine).where(Machine.id.in_(machine_ids))
        ).all()
        
        def hydrate(config_data, machine_dict):
            """
            replace tags in config with machine information. 
            (EX) {{tailscale_ip}} will be replaced with machine_object.tailscale_ip
            """
            config_str = json.dumps(config_data)
            # match all instances of {{token}} or {{token_alternate}}
            tokens = set(re.findall(r"\{\{([a-zA-Z_]+)\}\}", config_str))
            
            for token in tokens:
                if machine_dict.get(token):
                    config_str = config_str.replace(f'{{{{{token}}}}}', machine_dict.get(token))
            
            return json.loads(config_str)

        for machine_object in machine_objects:
                config = hydrate(data.get("spec"), machine_object.model_dump())
                background_tasks.add_task(
                    ContainerManager.send_agent_request,
                    address=machine_object.tailscale_ip,
                    method="POST",
                    endpoint=f"containers/create",
                    data=config
                )
                
    @staticmethod
    async def telemetry(id, session: Session):
        """
        Get cpu, memory, and storage usage of single machine or all active registered machines
        """
       
        
        async def fetch_agent_stats(client: httpx.AsyncClient, machine: Machine) -> dict:
            if not machine.tailscale_ip:
                raise ValueError("No valid Tailscale address configured")
                
            response = await client.get(f"http://{machine.tailscale_ip}:8001/system/usage", timeout=3.0)
            response.raise_for_status()
            return response.json()
        def parse_gb(val_str: str) -> float:
                if not val_str:
                    return 0.0
                return float(val_str.replace("GB", "").strip())
            
        async with httpx.AsyncClient() as client:
            if id is not None:
                machine = session.get(Machine, id)
                try:
                    stats = await fetch_agent_stats(client, machine)
                    return {"id": machine.id, "name": machine.user, "online": True, "stats": stats}
                except Exception as e:
                    return {"id": machine.id, "name": machine.name, "online": False, "error": str(e)}
    
            # Case 2: Aggregate / All machines requested
            machines = session.exec(select(Machine)).all()
            if not machines:
                return {"individual": [], "aggregate": {}}

            tasks = [fetch_agent_stats(client, m) for m in machines]
            results = await asyncio.gather(*tasks, return_exceptions=True)
    
            individual_stats = []
            total_cpu = 0.0
            total_ram_used_gb = 0.0
            total_ram_total_gb = 0.0
            total_storage_used_gb = 0.0
            total_storage_total_gb = 0.0 
            online_count = 0

            for machine, result in zip(machines, results):
                if isinstance(result, Exception):
                    individual_stats.append({
                        "id": machine.id, 
                        "name": machine.user, 
                        "online": False, 
                        "error": str(result)
                    })
                else:
                    online_count += 1
                   
                    individual_stats.append({
                        "id": machine.id, 
                        "name": machine.user, 
                        "online": True, 
                        "stats": result
                    })
                    
                    total_cpu += result.get("cpu", 0.0)
                    
                    if "memory" in result:
                        mem = result["memory"]
                        total_ram_used_gb += mem.get("used_gb", 0.0)
                        total_ram_total_gb += mem.get("total_gb", 0.0)
                    if "drives" in result:
                        for drive in result["drives"]:
                            total_storage_used_gb += drive.get("used_gb", 0.0)
                            total_storage_total_gb += drive.get("total_gb", 0.0)

            aggregate_metrics = {
                "total_machines": len(machines),
                "online_machines": online_count,
                "avg_cpu_percent": round(total_cpu / online_count, 1) if online_count > 0 else 0.0,
                "total_ram_used_gb": round(total_ram_used_gb, 2),
                "total_ram_total_gb": round(total_ram_total_gb, 2),
                "total_storage_used_gb": round(total_storage_used_gb, 2),
                "total_storage_total_gb": round(total_storage_total_gb, 2),
            }

            return {
                "individual": individual_stats,
                "aggregate": aggregate_metrics
            }
                

        




