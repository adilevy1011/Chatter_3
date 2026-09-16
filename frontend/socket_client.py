import asyncio
import os

import socketio


sio = socketio.AsyncClient(
    logger=True,
)

_connection_lock = asyncio.Lock()


async def ensure_connected():
    """Connect the server-side Flet session to the Socket.IO backend."""
    if sio.connected and "/" in sio.namespaces:
        return

    async with _connection_lock:
        if sio.connected and "/" in sio.namespaces:
            return

        if sio.connected:
            await sio.disconnect()

        await sio.connect(
            os.getenv("SOCKETIO_URL", "http://127.0.0.1:5678"),
            transports=["websocket"],
            namespaces=["/"],
        )
