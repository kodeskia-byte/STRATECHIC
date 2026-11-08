import os
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

BASE_DIR = Path(__file__).resolve().parent
INSTANCE_DIR = BASE_DIR / "instance"
INSTANCE_DIR.mkdir(exist_ok=True)

if load_dotenv is not None:
    load_dotenv(BASE_DIR / ".env")


def _secret_key():
    configured = os.environ.get("SECRET_KEY", "").strip()
    if configured:
        return configured
    path = INSTANCE_DIR / "secret_key"
    if path.exists():
        saved = path.read_text(encoding="utf-8").strip()
        if saved:
            return saved
    import secrets
    key = secrets.token_hex(32)
    path.write_text(key, encoding="utf-8")
    return key


def _database_uri():
    configured = os.environ.get("DATABASE_URL", "").strip()
    if configured.startswith("postgres://"):
        configured = "postgresql://" + configured[len("postgres://"):]
    if configured:
        return configured
    return "sqlite:///" + str(INSTANCE_DIR / "stratechic.db")


SQLALCHEMY_DATABASE_URI = _database_uri()
SQLALCHEMY_TRACK_MODIFICATIONS = False
if SQLALCHEMY_DATABASE_URI.startswith("sqlite"):
    SQLALCHEMY_ENGINE_OPTIONS = {"connect_args": {"timeout": 30}}

SECRET_KEY = _secret_key()
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_SECURE = os.environ.get("SESSION_COOKIE_SECURE", "0") == "1"
