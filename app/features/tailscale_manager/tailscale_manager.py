import requests
import os

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
        tailnet_ip = os_handler.install_tailscale(ssh_conn, hostname, self._get_access_token())

        return tailnet_ip
        
  
        
      




