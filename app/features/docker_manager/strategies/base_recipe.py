STRATEGY_REGISTRY = {}
import docker
def register_strategy(name):
    def decorator(cls):
        STRATEGY_REGISTRY[name] = cls
        return cls
    return decorator

class BaseDeploymentStrategy:
    def get_client(self, ip, user, port=22):
        """return DockerClient after establishing SSH connection remote machine\n
           :NOTE: This will not function if the target device and client device do not have
           SSH authentication setup
        """
        return docker.DockerClient(base_url=f"ssh://{user}@{ip}:{port}", use_ssh_client=True)
        
    def deploy(self, container_name, environment, images, machines):
        """Run docker container(s) on targeted machine(s), subclass must define this as environment variables, images, and the number
        of machines vary.
        """
        raise NotImplementedError
    
    def stop(self, machines):
        """
        Stop containers running the select strategy. Expects machines to be have the shape\n 
        machine = {"machine_object": Machine, "container_id": id, "role": machine_role}\n
        where machines = [machine_1, machine_2...machine_n]
        """
        for machine in machines:
            machine_obj = machine['machine_object']
            try:
                client = self.get_client(machine_obj.address, machine_obj.user, machine_obj.port)

                container = client.containers.get(container_id=machine["container_id"])
                container.remove(force=True)
                print(f" Removed {container.name} from {machine_obj.address}")
            except Exception as e:
                print(f"  Could not reach {machine_obj.address}: {str(e)}")   