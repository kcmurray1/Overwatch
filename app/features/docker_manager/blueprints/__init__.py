import os
import importlib

def register_blueprints():
    """Load all blueprints into BaseBlueprint's Registry"""
    folder = os.path.dirname(__file__)
    package_prefix = "app.features.docker_manager.blueprints"
    for file in os.listdir(folder):
        if file.endswith(".py") and file not in ["__init__.py", "base.py"]:
            module_name = file[:-3]
            full_module_path = f"{package_prefix}.{module_name}"
            importlib.import_module(full_module_path)

register_blueprints()