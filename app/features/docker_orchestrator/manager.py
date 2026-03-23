from .templates.base import BaseTemplate
from app.models import db, Project
from sqlalchemy import select, delete
from app.serializer import ProjectSchema
from app.core.errors import (MissingProjectFields, ProjectDoesNotExist)

class DockerOrchestrationManager:
    def __init__(self):
        self.registry = BaseTemplate._registry
        self.template_structures = BaseTemplate._structures

    def get_projects(self):
        projects = db.session.execute(select(Project)).scalars()
        return ProjectSchema(many=True).dump(projects)
    
    # FIXME: maybe return a receipt? FOr example to let user know what was shutdown and what wasn't in case of failure
    def stop_project(self, id):
        project = db.session.execute(select(Project).where(Project.id == id)).scalar_one_or_none()
        if not project:
            return ProjectDoesNotExist
        
        recipe = self.registry[project.strategy_type]
        
        machine_objects = Project.hydrate_machines(project.deployment_metadata)
        result = recipe().stop(machine_objects)
        project.is_running = False
        db.session.commit()
        return {}
    
    def get_project(self, id):
        project = db.session.execute(select(Project).where(Project.id == id)).scalar_one_or_none()
        if not project:
            raise ProjectDoesNotExist
        return ProjectSchema().dump(project)
    
    def remove_project(self, id):
        project = db.session.execute(select(Project).where(Project.id == id)).scalar_one_or_none()
        if not project:
            return ProjectDoesNotExist
        
        recipe = self.registry[project.strategy_type]
        
        machine_objects = Project.hydrate_machines(project.deployment_metadata)
        result = recipe().remove(machine_objects)
        db.session.execute(delete(Project).where(Project.id == id))
        db.session.commit()
        return {}

    def add_project(self, env, machines, images, template, name):
        """
        Create a docker container on targeted machine(s). Record the initial request and separately store
        the deployment_metadata of the created containers
        """
        # Can't add a project if template is unsupported or target machine is missing
        if not template or not machines:
            raise MissingProjectFields(message="Missing template and machine(s) selection")
        
        template_obj = self.registry[template]
     
        machines_cleaned = Project.hydrate_machines(machines)
 
        result = template_obj().create(name, env, images, machines_cleaned)
        print('deployment_metadata', result)

        new_project = Project(
            name=name,
            strategy_type=template,
        )  
        db.session.add(new_project)
        db.session.flush()
        new_project.config = {"env": env, "machines": machines, "images": images}
        new_project.deployment_metadata = result
        db.session.commit()
        return ProjectSchema().dump(new_project)
    
    def start_project(self, id):
        # get project
        project = db.session.execute(select(Project).where(Project.id == id)).scalar_one_or_none()

        if not project:
            raise ProjectDoesNotExist
        
        blueprint_obj = self.registry.get(project.strategy_type)
        if not blueprint_obj:
            # FIXME: check if invalid blueprint key
            pass
        print('hydrating..')
        updated_machines = Project.hydrate_machines(project.deployment_metadata)
        blueprint_obj().start(updated_machines)
        print('started..')
        project.is_running = True
        db.session.commit()
    

    def get_blueprints(self):
        return list(self.template_structures.values())
    

    