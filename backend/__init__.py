import socketio
import eventlet
import anthropic

from services.ai_service import generate_claude_message
sio = socketio.Server(
    cors_allowed_origins='*'
)

app = socketio.WSGIApp(sio)

messages =[]
@sio.event
def connect(sid, environ):
    print(f"Client connceted: {sid}")

@sio.event
def disconnect(sid):
    print(f"Client disconnected: {sid}")

@sio.on('ai_message')
def handle_message(sid, message):
    print(f"Message from {sid}: {message}")
    messages.append(
        {
            "role": "user",
            "content": message
        },
    )
    response = generate_claude_message(messages=messages)
    messages.append(
        {
            "role":"assistant",
            "content":response
        }
    )
    return response

if __name__=='__main__':
    print("Starting server...")
    eventlet.wsgi.server(eventlet.listen(('127.0.0.1',5678)),app)



