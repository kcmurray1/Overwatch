from .base import BaseTemplate
from app.models import Machine
from docker.errors import ImageNotFound
from dotenv import load_dotenv
import os

class CloudFlaredBlueprint(BaseTemplate):

    DEFAULT_IMAGE= "cloudflare/cloudflared:latest"

    def get_structure(self):
        return {"name": self.__name__, "struct": {"machine_roles": [{"name": "cloudflared", "many":False}]}}
    
    def create(self, container_name, environment, images, machines):
        load_dotenv()
        token = environment.get("token", os.environ.get("MY_TOKEN"))

        machine, = machines
        machine_obj = machine['machine_object']
        image = images[0] if images else self.DEFAULT_IMAGE

    
        client = self.get_client(machine_obj)
        try:
            client.images.get(image)
        except ImageNotFound:
            client.images.pull(image)

        client_container = client.containers.create(
            image=image,
            name=container_name,
            detach=True,
            command=f"tunnel --no-autoupdate run --token {token}",
            restart_policy={"Name": "always"}
        )

        return [{'container_id': client_container.id, 'id': machine_obj.id, 'role': machine['role']}]


    