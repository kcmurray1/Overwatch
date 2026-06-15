from .base import BaseTemplate
from dotenv import load_dotenv
import os

class MonitorTemplate(BaseTemplate):
 
    def get_structure(self):
        return {
            "name": self.__name__, 
            "struct": 
            {
                "machine_roles": [
                    {
                        "name": "monitor", 
                        "many":  False
                    }
                ]
            }
        }

    def create(self, container_name, environment, images, machines):
        
        container_configs = []

        FRONTEND_IMAGE=f'{os.environ.get('REGISTRY_HOST')}/overwatch-frontend:v1.2.0'
        APP_IMAGE=f'{os.environ.get('REGISTRY_HOST')}/overwatch-app:v1.2.0'

        for machine in machines:
            # create app container
            machine_obj = machine["machine_object"]
            container_key_path = f'/home/{machine_obj.user}/app/secrets/id_ecdsa'
            app_volumes = {
                # Mount the private key
                os.environ.get("KEY_PATH"): {
                    'bind': container_key_path, 
                    'mode': 'rw'
                },
                # CRITICAL: Mount the docker socket so the container can manage other containers
                '/var/run/docker.sock': {
                    'bind': '/var/run/docker.sock', 
                    'mode': 'rw'
                }
            }
            container_configs.append({
                'machine_role': machine['role'],
                'machine_object': machine['machine_object'],
                'config': {
                    'image': APP_IMAGE,
                    'name': f'{container_name}-monitor-app',
                    'detach':True,
                    'restart_policy': {"Name": "always"},
                    'user': 'root',
                    'volumes': app_volumes,
                    'environment': {
                        'KEY_PATH': container_key_path,
                        'DOCKER_HOST': 'unix:///var/run/docker.sock',
                        'DOCKER_SSH_SKIP_HOST_KEY_CHECK' : '1'
                    }
                }
            })

            # create frontend container
            container_configs.append({
                'machine_role': machine['role'],
                'machine_object': machine['machine_object'],
                'config': {
                    'image': FRONTEND_IMAGE,
                    'name': f'{container_name}-monitor-frontend',
                    'detach':True,
                    'restart_policy': {"Name": "always"},
                    'ports': {'80/tcp': 80},
                }
            })
            
            

        return super().create_helper(container_configs)
    
