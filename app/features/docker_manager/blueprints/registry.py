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

        port_binding = {"5000/tcp": (machine.tailscale_ip, 5000) if machine.tailscale_ip else environment.get("port", self.DEFAULT_REGISTRY_PORT)}
        
        client = self.get_client(machine_obj)
        client_container = client.containers.create(
            image=image,
            name=f'{container_name}-registry',
            detach=True,
            restart_policy={"Name": "always"},
            ports = port_binding
        )

        return [{'container_id': client_container.id, 'id': machine_obj.id, 'role': machine['role']}]


