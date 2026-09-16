import asyncio

import socketio

from frontend.runtime_config import get_backend_url


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
            get_backend_url(),
            transports=["websocket"],
            namespaces=["/"],
        )
