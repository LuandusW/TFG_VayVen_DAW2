from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from dotenv import load_dotenv

db = SQLAlchemy()
mail = Mail()

def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object("app.config.Config")
    
    db.init_app(app)
    mail.init_app(app)

    from app.routes.auth import auth_bp
    from app.routes.productos import productos_bp
    from app.routes.compra import compras_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(productos_bp)
    app.register_blueprint(compras_bp)

    @app.context_processor
    def inject_paypal():
        return dict(paypal_client_id=app.config["PAYPAL_CLIENT_ID"])

    return app