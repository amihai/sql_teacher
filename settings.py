"""Application settings module"""

import uuid
from pathlib import Path

class Settings:
    APP_NAME="teacher_agent"
    USER_ID="user"
    BASE_URL="http://localhost:8082"
    BASE_DIR=Path(__file__).parent

    @staticmethod
    def get_session_id():
        return str(uuid.uuid4())

settings = Settings()
