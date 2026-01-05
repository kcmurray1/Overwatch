from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os
from .models import db, Machine, Watchlist

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
    
    return app