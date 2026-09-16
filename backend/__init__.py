from fastapi import FastAPI
import flet.fastapi as flet_fastapi
from contextlib import asynccontextmanager
import socketio

from backend.sockets.ai_messages_sockets import register_ai_messages_sockets
from backend.sockets.lifecycle_sockets import register_lifecycle_sockets
from backend.sockets.auth_sockets import register_auth_sockets
from backend.config import sio

from frontend import main as flet_frontend_main
def create_app():
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        await flet_fastapi.app_manager.start()
        yield
        await flet_fastapi.app_manager.shutdown()
    app = FastAPI(lifespan=lifespan)
    app.mount("/socket.io", socketio.ASGIApp(sio))
    register_ai_messages_sockets()
    register_lifecycle_sockets()
    register_auth_sockets()
    app.mount("/", flet_fastapi.app(flet_frontend_main.main, assets_dir="assets"))
    return app
