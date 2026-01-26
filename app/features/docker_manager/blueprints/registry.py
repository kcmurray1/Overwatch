from .base_blueprint import BaseBlueprint

class DockerRegistryBlueprint(BaseBlueprint):
    DEFAULT_REGISTRY_IMAGE = "registry:3"
    DEFAULT_REGISTRY_PORT = 5000


    def create(self, container_name, environment, images, machines):
        machine, = machines
        machine_obj = machine['machine_object']
        image = images[0] if images else self.DEFAULT_REGISTRY_IMAGE
    
        client = self.get_client(machine_obj)
       
        client_container = client.containers.create(
            image=image,
            name=f'{container_name}-registry',
            detach=True,
            restart_policy={"Name": "always"},
            ports={f"5000/tcp":environment.get("port", self.DEFAULT_REGISTRY_PORT)}
        )

        return [{'container_id': client_container.id, 'id': machine_obj.id, 'role': machine['role']}]


