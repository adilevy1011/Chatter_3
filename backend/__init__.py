from fastapi import FastAPI
import socketio

from backend.sockets.ai_messages_sockets import register_ai_messages_sockets
from backend.sockets.lifecycle_sockets import register_lifecycle_sockets
from backend.sockets.auth_sockets import register_auth_sockets
from backend.config import sio

def create_app():
    app = FastAPI()
    app.mount("/socket.io", socketio.ASGIApp(sio))
    register_ai_messages_sockets()
    register_lifecycle_sockets()
    register_auth_sockets()
    return app
