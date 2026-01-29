BLUEPRINT_REGISTRY = {}
BLUEPRINT_STRUCTURES = {}
import docker
from abc import ABC, abstractmethod
class BaseBlueprint(ABC):

    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BLUEPRINT_STRUCTURES[cls.__name__] = cls.get_structure(cls) if cls.get_structure(cls) else {"name": cls.__name__}
        BLUEPRINT_REGISTRY[cls.__name__] = cls

    @abstractmethod
    def get_structure(self):
        pass
    
    def get_client(self, machine_obj):
        """return DockerClient after establishing SSH connection remote machine\n
           :NOTE: This will not function if the target device and client device do not have
           SSH authentication setup
        """
        return docker.DockerClient(base_url=f"ssh://{machine_obj.user}@{machine_obj.address}:{machine_obj.port}", use_ssh_client=True)
    
    def start(self, deployment_metadata):
        """Run docker container(s) on targeted machine(s), subclass must define this as environment variables, images, and the number
        of machines vary.
        """
        for machine in deployment_metadata:
            machine_obj = machine.get('machine_object')
            docker_client = self.get_client(machine_obj)
            project_container = docker_client.containers.get(machine['container_id'])
            project_container.start()
    
    @abstractmethod
    def create(self, container_name, environment, images, machines):
        """Create and push docker container provided the image, environment variables and name for the container.
           Each project is unique and may require this method to be overridden
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
                client = self.get_client(machine_obj)

                container = client.containers.get(container_id=machine["container_id"])
                container.remove(force=True)
                print(f" Removed {container.name} from {machine_obj.address}")
            except Exception as e:
                print(f"  Could not reach {machine_obj.address}: {str(e)}")   