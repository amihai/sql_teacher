"""Application settings module"""

import uuid
from pathlib import Path
import os
import logging

logging.basicConfig(level=logging.INFO)

class Settings:
    APP_NAME = "teacher_agent"
    APP_VERSION = "1.4.0"
    USER_ID = "user"
    BASE_URL = os.getenv("BASE_URL", "http://localhost:8082")
    BASE_DIR = Path(__file__).parent
    LOG_DIR = BASE_DIR / "logs"
    SESSION_DB = os.getenv("SESSION_DB", os.path.join(BASE_DIR, "session.db"))

    @staticmethod
    def get_session_id():
        return str(uuid.uuid4())

settings = Settings()
