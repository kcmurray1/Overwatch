import docker
from docker.errors import ImageNotFound
import time
from .base import BaseTemplate

class SeleniumGridBlueprint(BaseTemplate):
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

        container_configs = []
        for i, machine_metadata in enumerate(machines):
            machine_obj = machine_metadata["machine_object"]
            machine_role = machine_metadata["role"]
            container_config = { 
                'image': self.DEFAULT_HUB_IMAGE,
                'detach': True,
                'name' : f"{container_name}-hub",
                'ports': {'4442/tcp': 4442, '4443/tcp': 4443, '4444/tcp': 4444},
                'environment': {
                    "SE_EVENT_BUS_HOST": machine_obj.address,
                    "SE_EVENT_BUS_PUBLISH_PORT" : 4442,
                    "SE_EVENT_BUS_SUBSCRIBE_PORT": 4443
                    }
                } if machine_role == "hub" else {
                    'image': self.DEFAULT_NODE_IMAGE,
                    'name': f"{container_name}-node-{i}",
                    'shm_size': "10g",
                    'ports': {"5555/tcp":5555},
                    'detach': True,
                    'environment': {
                        "SE_EVENT_BUS_HOST": hub_obj.address,
                        "SE_NODE_HOST": machine_obj.address,
                        "SE_NODE_PORT":5555,
                        "SE_NODE_MAX_SESSIONS": self.DEFAULT_MAX_SESSIONS,
                        "SE_NODE_OVERRIDE_MAX_SESSIONS": "true"
                    }
                }
            container_configs.append(
                {
                    'machine_object': machine_obj,
                    'machine_role': machine_role,
                    'config': container_config
                })
        
        return super().create_helper(container_configs)

    



