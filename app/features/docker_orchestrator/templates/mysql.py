from .base import BaseTemplate
from docker.errors import ImageNotFound
import docker
class MySqlBlueprint(BaseTemplate):
    DEFAULT_REGISTRY_IMAGE = "100.95.32.60:5000/library/mysql:8.0"


    def get_structure(self):
        return {"name": self.__name__, "struct": {"machine_roles": [{"name": "mysql", "many":False}]}}

    def create(self, container_name, environment, images, machines):

        container_configs = []

        for machine in machines:
            container_configs.append({
                'machine_role': machine['role'],
                'machine_object': machine['machine_object'],
                'config': {
                    'image': self.DEFAULT_REGISTRY_IMAGE,
                    'name': f'{container_name}-mysql',
                    'detach':True,
                    'restart_policy': {"Name": "always"},
                    'ports': {'3306/tcp': 3306},
                    'environment': {
                        "MYSQL_ROOT_PASSWORD": "secret"
                    }
                }
            })
            
            

        return super().create_helper(container_configs)


