import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from werkzeug.middleware.proxy_fix import ProxyFix

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object("config")
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "admin.login"

    from .routes import main
    from .admin_routes import admin
    app.register_blueprint(main)
    app.register_blueprint(admin, url_prefix="/admin")

    with app.app_context():
        from .models import AdminUser, ContactMessage

        db.create_all()
        _ensure_admin()

        @login_manager.user_loader
        def load_user(user_id):
            return AdminUser.query.get(int(user_id))

    return app


def _ensure_admin():
    username = os.environ.get("ADMIN_USER", "").strip()
    password = os.environ.get("ADMIN_PASSWORD", "")
    if not username or not password:
        return
    from .models import AdminUser
    if AdminUser.query.filter_by(username=username).first():
        return
    user = AdminUser(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
