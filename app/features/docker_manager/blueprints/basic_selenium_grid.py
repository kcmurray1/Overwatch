import docker
from docker.errors import ImageNotFound
import time
from .base_blueprint import BaseBlueprint

class SeleniumGridBlueprint(BaseBlueprint):
    DEFAULT_HUB_IMAGE = "selenium/hub:4.39.0-20251212"
    DEFAULT_NODE_IMAGE = "selenium/node-chrome:4.39.0-20251212"
    DEFAULT_MAX_SESSIONS = 5


    def get_structure(self):
        return {"name": self.__name__, "struct": {"machine_roles": [{"name": "hub", "many":False}, {"name": "node", "many": True}]}}
        
    def create(self, container_name, environment, images, machines):
        """ {'name': 'test', 
            'recipe': 'SeleniumGridBlueprint', 
            'env': {'key': '', 'value': ''}, 
            'images': [], 
            'machines': [{'id': 1, 'role': 'hub', 'machine_object': <machine_obj>}, 
                        {'id': 2, 'role': 'node', 'machine_object': <machine_obj_two}, 
                        {'id': 3, 'role': 'node', 'machine_object': <machine_obj_three}]
        """ 
        # https://www.pythonmorsels.com/next/
        hub_obj = next(machine['machine_object'] for machine in machines if machine['role'] == 'hub')


        default_images = {"hub": SeleniumGridBlueprint.DEFAULT_HUB_IMAGE, "node": SeleniumGridBlueprint.DEFAULT_NODE_IMAGE}

        # check for images
        if images:
            hub_img = next(image for image in images if image['role'] == 'hub')
            node_img = next(image for image in images if image['role'] == 'node')
            hub_img = hub_img.get('name')
            node_img = node_img.get('name')

        operating_machines = []
        for i, machine_metadata in enumerate(machines):
            machine_obj = machine_metadata["machine_object"]
            machine_role = machine_metadata["role"]
            machine_image = default_images.get(machine_role)
            machine_client = self.get_client(machine_obj)
            try:
                machine_client.images.get(machine_image)
            except ImageNotFound:
                machine_client.images.pull(machine_image)
            machine_container = machine_client.containers.create(
                    machine_image,
                    detach=True,
                    name=f"{container_name}-hub",
                    ports={'4442/tcp': 4442, '4443/tcp': 4443, '4444/tcp': 4444},
                    environment={
                        "SE_EVENT_BUS_HOST": machine_obj.address,
                        "SE_EVENT_BUS_PUBLISH_PORT" : 4442,
                        "SE_EVENT_BUS_SUBSCRIBE_PORT": 4443
                    }
                ) if machine_role == "hub" else machine_client.containers.create(
                    machine_image,
                    name=f"{container_name}-node-{i}",
                    shm_size="10g",
                    ports={"5555/tcp":5555},
                    detach=True,
                    environment={
                        "SE_EVENT_BUS_HOST": hub_obj.address,
                        "SE_NODE_HOST":machine_obj.address,
                        "SE_NODE_PORT":5555,
                        "SE_NODE_MAX_SESSIONS": self.DEFAULT_MAX_SESSIONS,
                        "SE_NODE_OVERRIDE_MAX_SESSIONS": "true"
                    }
                )
           

            operating_machines.append({'container_id': machine_container.id, 'id' : machine_obj.id, 'role': machine_role})
        
        return operating_machines

    



