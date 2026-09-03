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
        ai_messages = [] #placeholder
        ai_messages.append(
            {
                "role": "user",
                "content": message
            },
        )
        response = generate_claude_message(messages=ai_messages)
        # ai_messages.append(
        #     {
        #         "role":"assistant",
        #         "content":response
        #     }
        # )
        return response