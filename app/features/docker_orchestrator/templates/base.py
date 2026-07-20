import docker
from abc import ABC, abstractmethod
from docker.errors import ImageNotFound

class BaseTemplate(ABC):
    _registry = {}
    _structures = {}
    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._structures[cls.__name__] = cls.get_structure(cls) if cls.get_structure(cls) else {"name": cls.__name__}
        cls._registry[cls.__name__] = cls

    # @abstractmethod
    def get_structure(self):
        pass
    
    def get_client(self, machine_obj):
        """return DockerClient after establishing SSH connection remote machine\n
           :NOTE: This will not function if the target device and client device do not have
           SSH authentication setup
        """
       
        print(f"connecting to ssh://{machine_obj.user}@{machine_obj.address}:{machine_obj.port}")
        return docker.DockerClient(base_url=f"ssh://{machine_obj.user}@{machine_obj.address}:{machine_obj.port}", use_ssh_client=True, version='auto', 
        timeout=60)

    
    def start(self, deployment_metadata):
        """Run docker container(s) on targeted machine(s), subclass must define this as environment variables, images, and the number
        of machines vary.
        """
        for machine in deployment_metadata:
            machine_obj = machine.get('machine_object')
            docker_client = self.get_client(machine_obj)
            project_container = docker_client.containers.get(machine['container_id'])
            project_container.start()
    
    # @abstractmethod
    def create(self, container_name, environment, images, machines):
        """Create and push docker container provided the image, environment variables and name for the container.
           Each project is unique and may require this method to be overridden
        """
        raise NotImplementedError
    
    def create_helper(self, container_configs):
        #NOTE: have the create wrapper assign images to machines per role

        created_containers = []
        for container_config in container_configs:
            machine_obj = container_config['machine_object']
            machine_role = container_config['machine_role']
            
            docker_client = self.get_client(machine_obj)
            
            config = container_config['config']

            machine_image = config['image']
            try:
                docker_client.images.get(machine_image)
            except ImageNotFound:
                docker_client.images.pull(machine_image)
                # maybe try to get image again to verify on machine otherwise throw error
            
            client_container = docker_client.containers.create(**config)

            created_containers.append(self.get_receipt(container=client_container, machine_obj=machine_obj, machine_role=machine_role))
        
        return created_containers

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
                container.stop()
                print(f" stopping.. {container.name} on {machine_obj.address}")
            except Exception as e:
                print(f"  Could not reach {machine_obj.address}: {str(e)}")   

    def remove(self, machines):
        """
        Remove container running on machine(s) associated with a container.\n
        Expects machines to be have the shape:\n 
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

    def get_receipt(self, container, machine_obj, machine_role):
        port_bindings = container.attrs['HostConfig']['PortBindings']
        
        network = {}
        for protocol in port_bindings:
            network['protocol'] = protocol

            for hostbinding in port_bindings[protocol]:
                network['host'] = hostbinding['HostIp']
                network['port'] = hostbinding['HostPort']

        return {'container_id': container.id, 'id': machine_obj.id, 'role': machine_role, 'network': network}
