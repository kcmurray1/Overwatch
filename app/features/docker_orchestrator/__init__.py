import os
import importlib

def register_templates():
    """Load all templates within the templates/ directory"""
    base_dir = os.path.dirname(__file__)
    template_dir = os.path.join(base_dir, 'templates')
    package_prefix = "app.features.docker_orchestrator.templates"
    for template in os.listdir(template_dir):
        if template.endswith(".py") and template not in ["__init__.py", "base.py"]:
            template_name = template[:-3]
            importlib.import_module(f"{package_prefix}.{template_name}")

register_templates()