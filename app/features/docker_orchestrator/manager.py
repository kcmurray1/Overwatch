from .templates.base import BaseTemplate
# from app.models import db, Project
from app.models_fast.model import Container, Machine
# from sqlalchemy import select, delete
# from app.serializer import ProjectSchema
from app.core.errors import (MissingProjectFields, ProjectDoesNotExist)
from sqlmodel import Session, select, delete

class DockerOrchestrationManager:
    def __init__(self):
        self.registry = BaseTemplate._registry
        self.template_structures = BaseTemplate._structures

    def get_info(self, machine_obj: Machine, session : Session):
        b = BaseTemplate()
        print("getting docker containers")
        docker_client = b.get_client(machine_obj=machine_obj)
        
        containers_to_add = []
        for container in docker_client.containers.list(all=True):
            container_info = container.attrs
            containers_to_add.append(Container(
                docker_id=container_info.get("Id"),
                image=container_info["Config"]["Image"],
                name=container_info.get("Name","").lstrip("/"),
                config=container_info.get("Config"),
                state=container_info["State"]["Status"],
                machine_id=machine_obj.id,
            ))
        
        session.add_all(containers_to_add)
        session.commit()


    def get_containers(self, session: Session):
        containers = session.exec(select(Container)).all()
        return [container.model_dump() for container in containers]
    
    # FIXME: maybe return a receipt? FOr example to let user know what was shutdown and what wasn't in case of failure
    def stop_project(self, id, session: Session):
        project = session.exec(select(Project).where(Project.id == id)).one_or_none()
        if not project:
            return ProjectDoesNotExist
        recipe = self.registry[project.strategy_type]
        
        machine_objects = Project.hydrate_machines(session, project.deployment_metadata)
        result = recipe().stop(machine_objects)
        project.is_running = False
        session.commit()
        return {}

    def get_container(self, id, session: Session):
        project = session.exec(select(Container).where(Container.id == id)).one_or_none()
        if not project:
            raise ProjectDoesNotExist

        return project.model_dump()
    
    # NOTE: this breaks if a machine is removed then re-added is it has a different id but the project config 
    # only remembers the machine's last ID
    def remove_container(self, id, session: Session):
        project = session.exec(select(Container).where(Container.id == id)).one_or_none()
        if not Container:
            return ProjectDoesNotExist
        
        recipe = self.registry[Container.strategy_type]
        machine_objects = Container.hydrate_machines(session, Container.deployment_metadata)
        result = recipe().remove(machine_objects)
        session.exec(delete(Container).where(Container.id == id))
        session.commit()
        return {}

    def add_container(self, data: dict, session: Session):
        # validate machine id and image name
        new_container = Container(
            docker_id=data.get("Id"),
            image=data["Config"]["Image"],
            name=data.get("Name","").lstrip("/"),
            config=data.get("Config"),
            state=data["State"]["Status"],
            machine_id=data.get("machind_id"),
        )
        session.add(new_container)
        session.commit()
        return new_container.model_dump()
    
    def add_project(self,session: Session, env, machines, images, template, name):
        # Can't add a project if template is unsupported or target machine is missing
        if not template or not machines:
            raise MissingProjectFields(message="Missing template and machine(s) selection")
        
        template_obj = self.registry[template]
     
        machines_cleaned = Project.hydrate_machines(session, machines)
 
        result = template_obj().create(name, env, images, machines_cleaned)
        print('deployment_metadata', result)

        new_project = Project(
            name=name,
            strategy_type=template,
        )  
        session.add(new_project)
        session.flush()
        
        new_project.config = {"env": env, "machines": machines, "images": images}
        new_project.deployment_metadata = result
        session.commit()
        return {"result": "dummy"}
    

    def start_project(self, id, session: Session):
        project = session.exec(select(Project).where(Project.id == id)).one_or_none()
        
        if not project:
            raise ProjectDoesNotExist
        
        blueprint_obj = self.registry.get(project.strategy_type)
        if not blueprint_obj:
            # FIXME: check if invalid blueprint key
            pass
        print('hydrating..')
        updated_machines = Project.hydrate_machines(session, project.deployment_metadata)
        blueprint_obj().start(updated_machines)
        print('started..')
        project.is_running = True
        session.commit()

    def get_blueprints(self):
        return list(self.template_structures.values())
    

    