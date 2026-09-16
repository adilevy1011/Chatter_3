from fastapi import FastAPI
import flet.fastapi as flet_fastapi
from contextlib import asynccontextmanager
from pathlib import Path
import socketio

from backend.sockets.ai_messages_sockets import register_ai_messages_sockets
from backend.sockets.lifecycle_sockets import register_lifecycle_sockets
from backend.sockets.auth_sockets import register_auth_sockets
from backend.config import sio

from frontend import main as flet_frontend_main


ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"


def create_app():
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        await flet_fastapi.app_manager.start()
        yield
        await flet_fastapi.app_manager.shutdown()
    app = FastAPI(lifespan=lifespan)
    register_ai_messages_sockets()
    register_lifecycle_sockets()
    register_auth_sockets()
    app.mount(
        "/",
        flet_fastapi.app(
            flet_frontend_main.main,
            assets_dir=str(ASSETS_DIR),
            app_name="Chatter",
            app_short_name="Chatter",
            app_description="Chat freely and securly on Chatter!",
        ),
    )
    return socketio.ASGIApp(sio, other_asgi_app=app)
