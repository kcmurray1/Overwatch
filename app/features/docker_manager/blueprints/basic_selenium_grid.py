import docker
import time
from .base_blueprint import BaseBlueprint

class SeleniumGridBlueprint(BaseBlueprint):
    DEFAULT_HUB_IMAGE = "selenium/hub:4.39.0-20251212"
    DEFAULT_NODE_IMAGE = "selenium/node-chrome:4.39.0-20251212"
    DEFAULT_MAX_SESSIONS = 5

    def deploy(self, container_name, environment, images, machines):
        deployment_metadata = {'machines': []}
        # environment will be basic k-v pairs
        # images and machines will follow the format [{machine: <machine_info>, "role": <any>}...] or [{"image_name": <img>}, "role": <any>}...]
        # https://www.pythonmorsels.com/next/
        hub = next(machine for machine in machines if machine['role'] == 'hub')
        nodes = [machine for machine in machines if machine['role'] == 'node']
        
        hub_img = SeleniumGridBlueprint.DEFAULT_HUB_IMAGE
        node_img = SeleniumGridBlueprint.DEFAULT_NODE_IMAGE
        # check for images
        if images:
            hub_img = next(image for image in images if image['role'] == 'hub')
            node_img = next(image for image in images if image['role'] == 'node')
            hub_img = hub_img.get('name')
            node_img = node_img.get('name')

        if environment:
            pass


        hub = hub['machine']
        hub_client = self.get_client(hub.address, hub.user, hub.port)
        hub_container = hub_client.containers.run(
            hub_img,
            detach=True,
            name=f"{container_name}-hub",
            ports={'4442/tcp': 4442, '4443/tcp': 4443, '4444/tcp': 4444},
            environment={
                "SE_EVENT_BUS_HOST": hub.address,
                "SE_EVENT_BUS_PUBLISH_PORT" : 4442,
                "SE_EVENT_BUS_SUBSCRIBE_PORT": 4443
            }
        )

        deployment_metadata['machines'].append({'container_id': hub_container.id, 'id' : hub.id, 'role': 'hub'})

        
        for i, node in enumerate(nodes):
            node = node['machine']
            client = self.get_client(node.address, node.user, node.port)
            
            # this should be updated to get the machine hardware to see how much memory it can spare and how many sessions it can handle
            node_container = client.containers.run(
                node_img,
                name=f"{container_name}-node-{i}",
                shm_size="10g",
                ports={"5555/tcp":5555},
                detach=True,
                environment={
                    "SE_EVENT_BUS_HOST":hub.address,
                    "SE_NODE_HOST":node.address,
                    "SE_NODE_PORT":5555,
                    "SE_NODE_MAX_SESSIONS": self.DEFAULT_MAX_SESSIONS,
                    "SE_NODE_OVERRIDE_MAX_SESSIONS": "true"
                }
            )

            
            deployment_metadata['machines'].append({'container_id': node_container.id, 'id': node.id, 'role': 'node'})

        return deployment_metadata
                

  
    



