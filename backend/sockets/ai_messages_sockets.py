import socketio
import eventlet
import anthropic
import sys
from pathlib import Path

from backend.services.ai_service import generate_claude_message
sys.path.append(str(Path(__file__).resolve().parent.parent))

from backend.config import sio
def register_ai_messages_sockets():
    @sio.on('ai_message')
    def handle_message(sid, message):
        print(f"Message from {sid}: {message}")
        response = generate_claude_message(message)
        return response