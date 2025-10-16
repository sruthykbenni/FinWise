# utils/session_manager.py
import secrets
import time

# Store tokens in memory for now (you can later persist in sqlite if needed)
SESSIONS = {}
SESSION_DURATION = 3600 * 3  # 3 hours

def create_session(username):
    token = secrets.token_urlsafe(32)
    SESSIONS[token] = {"user": username, "created": time.time()}
    return token

def validate_session(token):
    data = SESSIONS.get(token)
    if not data:
        return False
    if time.time() - data["created"] > SESSION_DURATION:
        del SESSIONS[token]
        return False
    return True

def get_user(token):
    if token in SESSIONS:
        return SESSIONS[token]["user"]
    return None

def clear_session():
    for t in list(SESSIONS.keys()):
        del SESSIONS[t]
