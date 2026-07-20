# from flask import Flask
# from flask_cors import CORS
# from dotenv import load_dotenv
# import os
# from .models import db
# from app.machine_manager import MachineManager
# from apscheduler.schedulers.background import BackgroundScheduler
# from datetime import datetime


# def create_app():
#     load_dotenv()
#     app = Flask(__name__)

#     # from .api_v1.views.machine import machine_bp
#     from .api_v1 import api_bp
#     from app.core.errors import (unexpected_error, machine_error, project_error, MachineError, ProjectError)
#     app.register_blueprint(api_bp)
#     app.register_error_handler(Exception, unexpected_error)
#     app.register_error_handler(MachineError, machine_error)
#     app.register_error_handler(ProjectError, project_error)

#     app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///machines.db"
#     key_path = os.getenv('KEY_PATH')

#     ssh_config_path = "/root/.ssh/config"
#     os.makedirs("/root/.ssh", exist_ok=True)
    
#     with open(ssh_config_path, "w") as f:
#         f.write(f"""
#             Host *
#                 IdentityFile {key_path}
#                 StrictHostKeyChecking no
#                 UserKnownHostsFile /dev/null
#                 IdentitiesOnly yes
#             """)
#     os.chmod(ssh_config_path, 0o600)
#     app.config['KEY_PATH'] = key_path
#     CORS(app)
#     db.init_app(app)

#     with app.app_context():
#         db.create_all()
    
#         scheduler = BackgroundScheduler()
#         scheduler.add_job(
#             func=MachineManager.check_connections,
#             trigger="interval",
#             seconds=15,
#             args=[app],
#             next_run_time=datetime.now(),
#             max_instances=1
#         )

#         scheduler.start()

#     return app