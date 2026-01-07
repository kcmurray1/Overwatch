from .base import BaseOS
import json
class LinuxOS(BaseOS):
    COMMANDS = {
        "SYS_INFO": [
            """hostnamectl --json=pretty""",
            """lscpu | grep "Model name" | cut -d : -f 2"""

                     
        ],
        "PROCESSES": """""",
    }


    def get_system_info(self, exec_handler):
        """Report Hardware, OS, Network Devices, etc."""

        # Build one large command to get system information
        # split each command by --- to split it in python
        master_cmd = """"""
        for sys_cmd in self.COMMANDS["SYS_INFO"]:
            master_cmd += sys_cmd + '; ' + """echo "---"; """
    
        raw_sys_info = exec_handler(master_cmd)

        sys_info, cpu, _ = raw_sys_info.split('---')

        sys_info = json.loads(sys_info)
        serialized_info = {}
       
        serialized_info["manufacturer"] = sys_info["HardwareVendor"]
        serialized_info["model"] = sys_info["HardwareModel"]
        serialized_info["os"] = sys_info["OperatingSystemPrettyName"]
        
        serialized_info["cpu"] = cpu.strip()
       
        
        return serialized_info
    

    def get_processes(self):
        """Get running applications/services"""
        pass

    def parse_output(self):
        """Report command execution results as json"""
        pass