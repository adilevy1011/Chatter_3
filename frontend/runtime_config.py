import os


LOCAL_BACKEND_URL = "http://127.0.0.1:5678"
PUBLIC_BACKEND_URL = "https://new.chatter-2.com"


def get_backend_url() -> str:
    """Return the Socket.IO endpoint for the current deployment."""
    return os.getenv(
        "CHATTER_BACKEND_URL",
        os.getenv("SOCKETIO_URL", LOCAL_BACKEND_URL),
    ).rstrip("/")
