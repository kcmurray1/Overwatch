import requests
import os
from app.core.os_platforms.windows import WindowsOS
from app.core.os_platforms.linux import LinuxOS

TOKEN_URL="https://api.tailscale.com/api/v2/oauth/token"

class TailscaleManager:
    def __init__(self, tags: list[str]):
        self.tags = tags

    def _get_access_token(self):
        res = requests.post(TOKEN_URL, data={
        "client_id": os.environ.get("TS_CL"),
        "client_secret": os.environ.get("TS_STUFF")
        })

        # https://tailscale.com/api#tag/keys/post/tailnet/{tailnet}/keys

        header = {"Authorization": f"Bearer {res.json().get('access_token')}"}

        # This payload defines the "properties" of the device joining
        payload = {
            "capabilities": {
                "devices": {
                    "create": {
                        "reusable": False,
                        "ephemeral": True,      
                        "preauthorized": True,  
                        "tags": self.tags 
                    }
                }
            },
            "expirySeconds": 3600 # Key expires if not used within 1 hour
        }
        res = requests.post("https://api.tailscale.com/api/v2/tailnet/-/keys", headers=header, json=payload)

        return res.json().get("key")
    
    def add_to_tailnet(self, ssh_conn, os_handler, hostname):
        """Execute OS-Based commands to install tailscale"""

        if isinstance(os_handler, WindowsOS):
            # NOTE: if windows device reaches NoState, likely needs manual authentication by signing in to machine
            # directly instead of over ssh
            stdin, stdout, stderr = ssh_conn.client.exec_command("tailscale ip -4")
            ts_ipv4 = stdout.read().decode()
            return ts_ipv4
        elif isinstance(os_handler, LinuxOS):
            print('handle linux')
            
            combined_cmd = f"""sudo -S curl -fsSL https://tailscale.com/install.sh | sh && sudo tailscale set --operator={hostname} && tailscale up --authkey={self._get_access_token()} --hostname={hostname} --accept-dns=false"""
            
            stdin, stdout, stderr = ssh_conn.client.exec_command(combined_cmd, get_pty=True)
            stdin.write(os.environ.get("CRED") + '\n')
            stdin.flush()
            print('err', stderr.read().decode())
        
            if stdout.channel.recv_exit_status() != 0:
                print("issue during tailscale installation...")
                return
            # returns tailscale ipv4 and unique ipv6(unused)
            stdin, stdout, stderr = ssh_conn.client.exec_command("tailscale ip")
            ts_ipv4, _  = stdout.read().decode().split()

            return ts_ipv4
        else:
            print('unsupported type ', type(os_handler))

        # tailnet_ip = os_handler.install_tailscale(ssh_conn, hostname, self._get_access_token())

        # return tailnet_ip
        
  
        
      
