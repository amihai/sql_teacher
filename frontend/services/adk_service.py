"""Services for consuming the API endpoints"""
from idlelib.debugger_r import DictProxy

import requests
import streamlit as st
from settings import settings
from typing import Dict, List


class ADKService:
    """Service class for Google ADK API interactions"""

    def __init__(self):
        self.base_url = settings.BASE_URL
        self.session = requests.Session()

    def create_session(self) -> Dict:
        """Create a new conversation session"""
        try:
            response = self.session.post(
                f"{self.base_url}/apps/{settings.APP_NAME}/users/{settings.USER_ID}/sessions/{settings.get_session_id()}"
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {}

    def get_session_by_id(self, session_id: str) -> List[Dict]:
        """Get a specific session by session id"""
        try:
            response = self.session.get(
                f"{self.base_url}/apps/{settings.APP_NAME}/users/{settings.USER_ID}/sessions/{session_id}"
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return []

    def get_sessions(self) -> List[Dict]:
        """Get all sessions"""
        try:
            response = self.session.get(
                f"{self.base_url}/apps/{settings.APP_NAME}/users/{settings.USER_ID}/sessions"
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return []



    def send_message(self, session_id: str, message: str) -> Dict:
        """Send a message to an agent in a session"""

        try:
            payload = {
                "appName": settings.APP_NAME,
                "userId": settings.USER_ID,
                "sessionId": session_id,
                "newMessage": {
                    "role": "user",
                    "parts": [{"text": message}]
                }
            }
            response = self.session.post(f"{self.base_url}/run", json=payload)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

    def delete_session(self, session_id: str):
        """Delete a specific session"""
        try:
            response = self.session.delete(
                f"{self.base_url}/apps/{settings.APP_NAME}/users/{settings.USER_ID}/sessions/{session_id}"
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

