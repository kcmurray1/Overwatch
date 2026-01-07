from .base import BaseOS
import json

class WindowsOS(BaseOS):

    COMMANDS = {
        "SYS_INFO": """powershell "Get-ComputerInfo | ConvertTo-Json" """,
        "PROCESSES": """powershell "get-process | Sort-Object CPU -Descending | Select-Object -First 10 -Property Name, Id, CPU | ConvertTo-Json" """
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

        # FIXME: add these in the future
        # storage

        # ram
        return serialized_info
    

    def get_processes(self, exec_fun):
        """Get running applications/services"""
        processes =  exec_fun(self.COMMANDS['PROCESSES'])

        return json.loads(processes)

    def parse_output(self):
        """basic parser to convert command execution results as json"""
        pass

    def get_os_cmd(self):
        return """powershell "Get-ComputerInfo -Property OsName | ConvertTo-Json " """