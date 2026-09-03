import socketio
import eventlet

from sockets.ai_messages_sockets import register_ai_messages_sockets
from sockets.lifecycle_sockets import register_lifecycle_sockets

from services.ai_service import generate_claude_message
from config import sio



def create_app():
    app = socketio.WSGIApp(sio)

    register_ai_messages_sockets()
    register_lifecycle_sockets()

    return app





