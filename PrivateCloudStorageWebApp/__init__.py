from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    with app.app_context():
        app.config['SECRET_KEY'] = 'secret-key-goes-here'
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
        app.config['MAIL_SERVER'] = 'smtp.gmail.com'
        app.config['MAIL_PORT'] = 465
        app.config['MAIL_USE_SSL'] = True
        app.config['MAIL_USE_TLS'] = False
        app.config['MAIL_USERNAME'] = 'yesyes02000@gmail.com'
        app.config['MAIL_PASSWORD'] = 'yesyesyes00'
        db.init_app(app)
        from .auth import auth as auth_blueprint
        app.register_blueprint(auth_blueprint)
        from .cloud import cloud as cloud_blueprint
        app.register_blueprint(cloud_blueprint)
        from .main import main as main_blueprint
        app.register_blueprint(main_blueprint)
        db.init_app(app)
        login_manager = LoginManager()
        login_manager.login_view = 'auth.login'
        login_manager.init_app(app)
        from .models import User
        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))
    return app
