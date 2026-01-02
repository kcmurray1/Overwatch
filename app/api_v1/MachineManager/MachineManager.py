import paramiko
import json




class MachineManager:
    @staticmethod
    def machine_info(ssh_client, machine=None):

        cmd = """powershell "Get-ComputerInfo | ConvertTo-Json" """


        sys_info = MachineManager._execute(ssh_client, cmd)
        
        sys_info = json.loads(sys_info)


        serialized_info = dict()

        # Windows have different paremeters based on version
        
        # # Uptime
        serialized_info["uptime"] = sys_info["OsUptime"]        
        # # OS ver
        serialized_info["os"] = sys_info["OsName"]
        # # addr
        serialized_info["addr"] = [{"connectionid" : adapter['ConnectionID'], "description": adapter['Description'], "address" : adapter['IPAddresses']} for adapter in sys_info["CsNetworkAdapters"]]
        # # CPU
        serialized_info["cpu"] = sys_info["CsProcessors"][0]["Name"]
        # # user
        # serialized_info["user"] = sys_info["CsPrimaryOwnerName"]
        return serialized_info
        
    def get_running_services(ssh_client, offset=None):
        cmd = """powershell "get-process | Sort-Object CPU -Descending | Select-Object -First 10 -Property Name, Id, CPU | ConvertTo-Json" """
        if offset:
            cmd = f"""powershell "get-process | Sort-Object CPU -Descending | Select-Object -First 5 -Skip {offset} -Property Name, Id, CPU | ConvertTo-Json" """
        return MachineManager._execute(ssh_client, cmd)

    def get_status(ssh_client : paramiko.SSHClient, machine=None):
        # get machine info(including os)
        info = MachineManager.machine_info(ssh_client)

        services = MachineManager.get_running_services(ssh_client)
        return {"info" : info, "running" : json.loads(services)}

    
    @staticmethod
    def _execute(client, command):
        stdin, stdout, stderr = client.exec_command(command)

        return stdout.read().decode().strip()


