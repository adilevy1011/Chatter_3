import sys
from pathlib import Path
from flask import request

sys.path.append(str(Path(__file__).resolve().parent.parent))

from backend.config import sio
def register_lifecycle_sockets():
    @sio.on('connect')
    def connect():
        print(f"Client connceted: {request.sid}")

    @sio.on('disconnect')
    def disconnect():
        print(f"Client disconnected: {request.sid}")