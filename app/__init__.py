from flask import Flask
from dotenv import load_dotenv
import os
def create_app():
    load_dotenv()
    app = Flask(__name__)

    from .api_v1.views.machine import machine_bp

    app.register_blueprint(machine_bp)

    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///:memory:"
    app.config['KEY_PATH'] = os.environ.get("KEY_PATH")
    return app