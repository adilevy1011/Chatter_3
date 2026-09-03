import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from backend.config import sio
def register_lifecycle_sockets():
    @sio.event
    def connect(sid, environ):
        print(f"Client connceted: {sid}")

    @sio.event
    def disconnect(sid):
        print(f"Client disconnected: {sid}")