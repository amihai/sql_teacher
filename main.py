import os
from google.adk.cli.fast_api import get_fast_api_app
from fastapi import FastAPI
from settings import settings
from pathlib import Path

AGENT_DIR = str(Path(__file__).resolve().parent / "backend")
SESSION_DB_URL = f"sqlite:///{os.path.join(settings.BASE_DIR, "sessions.db")}"

# Create FastAPI app with enabled cloud tracing
app: FastAPI = get_fast_api_app(
    agents_dir=AGENT_DIR,
    session_service_uri=SESSION_DB_URL,
    allow_origins=["*"],
    artifact_service_uri=None,
    web=True,
)

app.title = "teacher-agent"
app.description = "API for interacting with the Agent teacher-agent"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)