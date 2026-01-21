from .base_recipe import BaseDeploymentStrategy, register_strategy

@register_strategy("Registry")
class DockerRegistry(BaseDeploymentStrategy):
    DEFAULT_REGISTRY_IMAGE = "registry:3"
    DEFAULT_REGISTRY_PORT = 5000

    def deploy(self, container_name, environment, images, machines): 
        deployment_metadata = {'machines': []}
        machine, = machines
        machine_obj = machine['machine']
        try:
            image, = images
        except ValueError:
            image = self.DEFAULT_REGISTRY_IMAGE
            
        client = self.get_client(machine_obj.address, machine_obj.user, machine_obj.port)
       
        client_container = client.containers.run(
            image=image,
            name=f'{container_name}-registry',
            detach=True,
            restart_policy={"Name": "always"},
            ports={f"5000/tcp":environment.get("port", self.DEFAULT_REGISTRY_PORT)}
        )
        deployment_metadata['machines'].append({'container_id': client_container.id, 'id': machine_obj.id, 'role': machine['role']})

        return deployment_metadata
     
