import docker
import time
class BasicSeleniumGrid:

    def __init__(self, project_name="default-basic-selenium-grid"):
        self.HUB_IMAGE =  "selenium/hub:4.39.0-20251212"
        self.NODE_IMAGE =  "selenium/node-chrome:4.39.0-20251212"
        self.PROJECT_NAME = project_name
        self.hub = None
        self.nodes = None

    def get_client(self, ip, user, port=22):
        return docker.DockerClient(base_url=f"ssh://{user}@{ip}:{port}", use_ssh_client=True)
    
    def deploy(self, config):
        print("deploying...", config)
        """EX:) config = {hub: {address: '10.0.0.42', user: 'bobby'}, nodes: [{address: 10.0.0.5, user: 'alice'}]}"""
        hub = config["hub"]
        hub_address = hub.get('address')
        hub_user = hub.get('user')
        nodes = config["nodes"]

        hub_client = self.get_client(hub_address, hub_user)

        # start the hub container
        hub_client.containers.run(
            self.HUB_IMAGE,
            detach=True,
            name=f"{self.PROJECT_NAME}-hub",
            ports={'4442/tcp': 4442, '4443/tcp': 4443, '4444/tcp': 4444},
            environment={
                "SE_EVENT_BUS_HOST": hub_address,
                "SE_EVENT_BUS_PUBLISH_PORT" : 4442,
                "SE_EVENT_BUS_SUBSCRIBE_PORT": 4443
            }
        )


        # Give the Hub a moment to initialize before nodes connect
        time.sleep(3)

        for i, node in enumerate(nodes):
            client = self.get_client(node['address'], node['user'], node['port'])
            
            # this would be updated to get the machine hardware to see how much memory it can spare and how many sessions it can handle
            client.containers.run(
                self.NODE_IMAGE,
                name=f"{self.PROJECT_NAME}-node-{i}",
                shm_size="10g",
                ports={"5555/tcp":5555},
                detach=True,
                environment={
                    "SE_EVENT_BUS_HOST":hub_address,
                    "SE_NODE_HOST":node['address'],
                    "SE_NODE_PORT":5555,
                    "SE_NODE_MAX_SESSIONS": 4,
                    "SE_NODE_OVERRIDE_MAX_SESSIONS": "true"
                }
            )


    def stop(self, config):
        print("stopping...")
        hub = config["hub"]
        nodes = config["nodes"]
        for node in nodes:
            try:
                client = self.get_client(node['address'], node['user'], node['port'])
                containers = client.containers.list(all=True, filters={"name": f"{self.PROJECT_NAME}-"})
                for c in containers:
                    print(f"  Removing {c.name} from {node['address']}...")
                    c.remove(force=True)
            except Exception as e:
                print(f"  Could not reach {node['address']}: {e}")

    
        try:
            client = self.get_client(hub['address'], hub['user'])
            containers = client.containers.list(all=True, filters={"name": f"{self.PROJECT_NAME}-"})
            for c in containers:
                print(f"  Removing {c.name} from {hub['address']}...")
                c.remove(force=True)
        except Exception as e:
            print(f"  Could not reach {hub['address']}: {e}")

  
    



