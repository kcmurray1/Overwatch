from .base import BaseOS
import json

class WindowsOS(BaseOS):

    COMMANDS = {
        "SYS_INFO": """powershell "Get-ComputerInfo | ConvertTo-Json" """,
        "PROCESSES": """powershell "get-process | Sort-Object CPU -Descending | Select-Object -First 10 -Property Name, Id, CPU | ConvertTo-Json" """,
        "RESTART" : """powershell "Restart-Computer" """
    }

    def get_system_info(self, exec_fun):
        """Report Hardware, OS, Network Devices, etc."""

        sys_info = exec_fun(self.COMMANDS['SYS_INFO'])

        sys_info = json.loads(sys_info)
        serialized_info = {}
     
        # OS ver
        serialized_info["os"] = sys_info["OsName"]
        # addr(into a list since there can be multiple network interfaces on a single device)
        serialized_info["address"] = [{"connectionid" : adapter['ConnectionID'], "description": adapter['Description'], "address" : adapter['IPAddresses']} for adapter in sys_info["CsNetworkAdapters"]]
        # CPU
        serialized_info["cpu"] = sys_info["CsProcessors"][0]["Name"]
        # manufacturer
        serialized_info["model"] = sys_info["CsModel"]
        # model
        serialized_info["manufacturer"] = sys_info["CsManufacturer"]

        return serialized_info
    

    def get_processes(self, exec_fun):
        """Get running applications/services"""
        processes =  exec_fun(self.COMMANDS['PROCESSES'])

        return json.loads(processes)

    def restart(self, exec_fun):
        print("restarting... windows")
        exec_fun(self.COMMANDS['RESTART'])
        return 
    
    def stop(self, exec_fun):
        pass

    def install_tailscale(self, exec_func, hostname, access_token):

        stdin, stdout, stderr = exec_func.client.exec_command("tailscale ip -4")
        ts_ipv4 = stdout.read().decode()

        return ts_ipv4