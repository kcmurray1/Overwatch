"""
Docstring for app.features.docker_manager.strategies.cloudflared

"""
from .base_recipe import BaseDeploymentStrategy, register_strategy
from app.models import Machine
import docker
from dotenv import load_dotenv
import os
@register_strategy("CloudFlared")
class CloudFlared(BaseDeploymentStrategy):

    DEFAULT_IMAGE= "cloudflare/cloudflared:latest"
    def deploy(self, container_name, environment, images, machines):
        load_dotenv()
        deployment_metadata = {"machines": []}
        token = environment.get("token", os.environ.get("MY_TOKEN"))
        machine, = machines
        machine_obj = machine['machine']
        try:
            image, = images
        except ValueError:
            image = self.DEFAULT_IMAGE
       
        client = self.get_client(machine_obj.address, machine_obj.user, machine_obj.port)

       
        client_container = client.containers.run(
            image=image,
            name=container_name,
            detach=True,
            command=f"tunnel --no-autoupdate run --token {token}",
            restart_policy={"Name": "always"}
        )

        deployment_metadata['machines'].append({'container_id': client_container.id, 'id': machine_obj.id, 'role': machine['role']})

        return deployment_metadata


    