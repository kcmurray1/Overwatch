from .base_blueprint import BaseBlueprint
from docker.errors import ImageNotFound
import docker
class MySqlBlueprint(BaseBlueprint):
    DEFAULT_REGISTRY_IMAGE = "100.95.32.60:5000/library/mysql:8.0"


    def get_structure(self):
        return {"name": self.__name__, "struct": {"machine_roles": [{"name": "mysql", "many":False}]}}

    def create(self, container_name, environment, images, machines):
        machine, = machines
        machine_obj = machine['machine_object']
        image = images[0] if images else self.DEFAULT_REGISTRY_IMAGE
        print("creating registry port..", flush=True)
      
        print("done binding...", flush=True)
       
        print("getting client...", flush=True)

        
           
        client = self.get_client(machine_obj)
        client.images.pull(image)
        print("creating mysql..", flush=True)
        client_container = client.containers.create(
            image=image,
            name=f'{container_name}-mysql',
            detach=True,
            restart_policy={"Name": "always"},
            ports={'3306/tcp': 3306},
            environment={
                "MYSQL_ROOT_PASSWORD": "secret"
            }
        )

        return [{'container_id': client_container.id, 'id': machine_obj.id, 'role': machine['role']}]


