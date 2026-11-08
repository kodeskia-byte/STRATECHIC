import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

os.environ.setdefault("FLASK_ENV", "production")
os.environ.setdefault("SESSION_COOKIE_SECURE", "1")

log_dir = os.path.join(BASE_DIR, "tmp")
os.makedirs(log_dir, exist_ok=True)

from app import create_app

application = create_app()

try:
    import logging
    from logging.handlers import RotatingFileHandler

    handler = RotatingFileHandler(
        os.path.join(log_dir, "wsgi_error.log"),
        maxBytes=1_000_000,
        backupCount=3,
    )
    handler.setLevel(logging.INFO)
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s: %(message)s"))
    application.logger.addHandler(handler)
    application.logger.setLevel(logging.INFO)
except Exception:
    pass
