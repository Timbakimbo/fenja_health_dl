import os
import secrets

from dotenv import load_dotenv
from fastapi import Header, HTTPException

load_dotenv()

API_KEY = os.environ.get("API_KEY", "")


def verify_api_key(x_api_key: str = Header(...)) -> None:
    if not API_KEY or not secrets.compare_digest(x_api_key, API_KEY):
        raise HTTPException(status_code=403, detail="Invalid or missing API key")
