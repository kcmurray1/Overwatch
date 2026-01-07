from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os
from .models import db,Machine
# learning apscheduler
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import select
from datetime import datetime
import paramiko
def foo(app):
    with app.app_context():
        print("polling...")
        machines = db.session.execute(select(Machine)).scalars()
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        for machine in machines:
            try:
                client.connect(machine.address, port=machine.port,  username=machine.user, key_filename=app.config["KEY_PATH"], timeout=5)
                machine.is_online = True
            except:
                machine.is_online = False
            finally:
                db.session.commit()
                client.close()

def create_app():
    load_dotenv()
    app = Flask(__name__)

    from .api_v1.views.machine import machine_bp

    app.register_blueprint(machine_bp)

    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///machines.db"
    app.config['KEY_PATH'] = os.environ.get("KEY_PATH")

    CORS(app)
    db.init_app(app)

    with app.app_context():
        db.create_all()
    
        scheduler = BackgroundScheduler()
        scheduler.add_job(
            func=foo,
            trigger="interval",
            seconds=10,
            args=[app],
            next_run_time=datetime.now(),
            max_instances=1
        )

        scheduler.start()

    return app