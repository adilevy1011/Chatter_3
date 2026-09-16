from backend.config import sio

def register_lifecycle_sockets():
    @sio.on('connect')
    async def connect(sid, environ):
        print(f"Client connected: {sid}")

    @sio.on('disconnect')
    async def disconnect(sid):
        print(f"Client disconnected: {sid}")