STRATEGY_REGISTRY = {}

def register_strategy(name):
    def decorator(cls):
        STRATEGY_REGISTRY[name] = cls
        return cls
    return decorator

class BaseDeploymentStrategy:
    def deploy(self):
        raise NotImplementedError