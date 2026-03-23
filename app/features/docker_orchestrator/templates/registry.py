from .base import BaseTemplate

class DockerRegistryBlueprint(BaseTemplate):
    DEFAULT_REGISTRY_IMAGE = "registry:3"
    DEFAULT_REGISTRY_PORT = 5000
    

    def get_structure(self):
        return {"name": self.__name__, "struct": {"machine_roles": [{"name": "registry", "many":False}]}}
    
    def create(self, container_name, environment, images, machines):
        
        container_configs = []

        image = self.DEFAULT_REGISTRY_IMAGE
        # NOTE: enter except if missing tailscale_ip
        for machine in machines:
            machine_obj = machine['machine_object']

            port_binding = {"5000/tcp": (machine_obj.tailscale_ip, 5000)}
            volumes_config = {
                f"/var/lib/docker-registry/{container_name}": {
                    'bind': '/var/lib/registry',
                    'mode': 'rw'                 
                }
            }
            container_configs.append({
                'machine_object': machine_obj,
                'machine_role': machine['role'],
                'config' : {
                    'image': image,
                    'name': f'{container_name}-registry',
                    'volumes': volumes_config,
                    'ports':  port_binding,
                    'environment': {
                        "REGISTRY_STORAGE_DELETE_ENABLED": "true"
                    }
                }
            })

        
        return super().create_helper(container_configs=container_configs)


