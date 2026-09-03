import socketio
import eventlet
import anthropic
import sys
from pathlib import Path

from services.ai_service import generate_claude_message
from services.supabase_service import ai_messages
sys.path.append(str(Path(__file__).resolve().parent.parent))

from config import sio
def register_ai_messages_sockets():
    @sio.on('ai_message')
    def handle_message(sid, message):
        print(f"Message from {sid}: {message}")
        ai_messages.append(
            {
                "role": "user",
                "content": message
            },
        )
        response = generate_claude_message(messages=ai_messages)
        ai_messages.append(
            {
                "role":"assistant",
                "content":response
            }
        )
        return response