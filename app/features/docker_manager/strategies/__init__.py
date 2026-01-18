import os
import importlib

def discover_strategies():
    folder = os.path.dirname(__file__)
    package_prefix = "app.features.docker_manager.strategies"

    for file in os.listdir(folder):
        if file.endswith(".py") and file not in ["__init__.py", "base.py"]:
            # ignore .py in filename
            module_name = file[:-3]
            full_module_path = f"{package_prefix}.{module_name}"
            
            # This triggers the @register_strategy decorator
            importlib.import_module(full_module_path)
# load packages
discover_strategies()