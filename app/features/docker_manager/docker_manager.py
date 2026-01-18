import docker
# from .strategies.basic_selenium_grid import BasicSeleniumGrid
class DockerManager:
    def __init__(self, strategy_name):
        pass
    
    def deploy(self, config):
        self.strategy.deploy(config=config)

    def stop(self, config):
        self.strategy.stop(config)
   
