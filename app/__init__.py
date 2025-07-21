import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config # Asegúrate de que esta línea esté presente

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config) 

    db.init_app(app)

    # ¡Importación cambiada!
    from app.routes.web_routes import bp as main_bp 
    app.register_blueprint(main_bp)

    with app.app_context():
        instance_path = os.path.join(app.root_path, 'instance')
        if not os.path.exists(instance_path):
            os.makedirs(instance_path)

    return app