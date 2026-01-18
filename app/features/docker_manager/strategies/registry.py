from .base import BaseDeploymentStrategy, register_strategy

@register_strategy("Registry")
class DockerRegistry(BaseDeploymentStrategy):
     def deploy(self):
         pass
     
