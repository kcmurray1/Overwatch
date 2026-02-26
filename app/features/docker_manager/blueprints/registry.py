from .base_blueprint import BaseBlueprint

class DockerRegistryBlueprint(BaseBlueprint):
    DEFAULT_REGISTRY_IMAGE = "registry:3"
    DEFAULT_REGISTRY_PORT = 5000
    

    def get_structure(self):
        return {"name": self.__name__, "struct": {"machine_roles": [{"name": "registry", "many":False}]}}

    def create(self, container_name, environment, images, machines):
        machine, = machines
        machine_obj = machine['machine_object']
        image = images[0] if images else self.DEFAULT_REGISTRY_IMAGE
        print("creating registry port..", flush=True)
        port_binding = {"5000/tcp": (machine_obj.tailscale_ip, 5000) if machine_obj.tailscale_ip else environment.get("port", self.DEFAULT_REGISTRY_PORT)}
        print("done binding...", flush=True)
        volumes_config = {
            f"/var/lib/docker-registry/{container_name}": {
                'bind': '/var/lib/registry',
                'mode': 'rw'                 
            }
        }
        print("getting client...", flush=True)
        client = self.get_client(machine_obj)
        print("creating registry..", flush=True)
        client_container = client.containers.create(
            image=image,
            name=f'{container_name}-registry',
            detach=True,
            restart_policy={"Name": "always"},
            volumes=volumes_config,
            ports = port_binding,
            environment={
                "REGISTRY_STORAGE_DELETE_ENABLED": "true"
            }
        )

        return [{'container_id': client_container.id, 'id': machine_obj.id, 'role': machine['role']}]


