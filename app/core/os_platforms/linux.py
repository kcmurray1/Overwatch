from .base import BaseOS
import json
import os

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

    def restart(self):
        pass

    def stop(self):
        pass

    def install_tailscale(self, exec_func, hostname, access_token):
        print("adding tailscale to machine...")
        combined_cmd = f"""sudo -S curl -fsSL https://tailscale.com/install.sh | sh && sudo tailscale set --operator={hostname} && tailscale up --authkey={access_token} --hostname={hostname} --accept-dns=false"""
        
        stdin, stdout, stderr = exec_func.client.exec_command(combined_cmd, get_pty=True)
        stdin.write(os.environ.get("CRED") + '\n')
        stdin.flush()
        print('err', stderr.read().decode())
    
        if stdout.channel.recv_exit_status() != 0:
            print("issue during tailscale installation...")
            return
        # returns tailscale ipv4 and unique ipv6(unused)
        stdin, stdout, stderr = exec_func.client.exec_command("tailscale ip")
        ts_ipv4, _  = stdout.read().decode().split()

        return ts_ipv4

        

        

     
    
