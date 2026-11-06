import requests
import logging

logger = logging.getLogger(__name__)

from app.core.os_platforms.windows import WindowsOS
from app.core.os_platforms.linux import LinuxOS
from app.core.configs.settings import get_settings


class TailscaleManager:
    TOKEN_URL="https://api.tailscale.com/api/v2/oauth/token"
    DEVICE_TOKEN_URL = "https://api.tailscale.com/api/v2/tailnet/-/keys"
    
    
    def __init__(self, tags: list[str]):
        self.tags = tags

    def _get_access_token(self, ephemeral=True, reusable=False):
        res = requests.post(self.TOKEN_URL, data={
        "client_id": get_settings().ts_cl,
        "client_secret": get_settings().ts_stuff
        })

        # https://tailscale.com/api#tag/keys/post/tailnet/{tailnet}/keys

        header = {"Authorization": f"Bearer {res.json().get('access_token')}"}

        # This payload defines the "properties" of the device joining
        payload = {
            "capabilities": {
                "devices": {
                    "create": {
                        "reusable": reusable,
                        "ephemeral": ephemeral,      
                        "preauthorized": True,  
                        "tags": self.tags 
                    }
                }
            },
            "expirySeconds": 3600 # Key expires if not used within 1 hour
        }
        res = requests.post(self.DEVICE_TOKEN_URL, headers=header, json=payload)
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
            access_token = self._get_access_token()
            combined_cmd = f"""sudo -S curl -fsSL https://tailscale.com/install.sh | sh && sudo tailscale set --operator={hostname} && tailscale up --authkey={access_token} --hostname={hostname} --accept-dns=false"""
            
            stdin, stdout, stderr = ssh_conn.client.exec_command(combined_cmd, get_pty=True)
            stdin.write(get_settings().cred + '\n')
            stdin.flush()
            
            logger.error(f'Tailnet os error: {stderr.read().decode()}')
        
            
        
            if stdout.channel.recv_exit_status() != 0:
                logger.error("issue during tailscale installation...")
                return
            # returns tailscale ipv4 and unique ipv6(unused)
            stdin, stdout, stderr = ssh_conn.client.exec_command("tailscale ip")
            ts_ipv4, _  = stdout.read().decode().split()

            return ts_ipv4
        else:
            logger.warning('unsupported type ', type(os_handler))

        # tailnet_ip = os_handler.install_tailscale(ssh_conn, hostname, self._get_access_token())

        # return tailnet_ip
        
  
        
      
