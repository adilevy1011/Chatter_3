from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
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

SOCIAL_PREVIEW_TAGS = """
<meta property="og:title" content="Chatter">
<meta property="og:description" content="Chat with AI using Chatter.">
<meta property="og:type" content="website">
<meta property="og:url" content="https://new.chatter-2.com/">
<meta property="og:image" content="https://new.chatter-2.com/social-preview.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">

<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Chatter">
<meta name="twitter:description" content="Chat with AI using Chatter.">
<meta name="twitter:image" content="https://new.chatter-2.com/social-preview.png">
"""


class SocialPreviewMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        content_type = response.headers.get("content-type", "")
        if (
            request.method != "GET"
            or response.status_code != 200
            or "text/html" not in content_type
        ):
            return response

        chunks = [chunk async for chunk in response.body_iterator]
        html = b"".join(chunks).decode("utf-8")

        if "</head>" in html:
            html = html.replace(
                "</head>",
                f"{SOCIAL_PREVIEW_TAGS}\n</head>",
                1,
            )

        headers = dict(response.headers)
        headers.pop("content-length", None)
        headers.pop("content-type", None)

        return Response(
            content=html,
            status_code=response.status_code,
            headers=headers,
            media_type="text/html",
            background=response.background,
        )

def create_app():
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        await flet_fastapi.app_manager.start()
        yield
        await flet_fastapi.app_manager.shutdown()
    app = FastAPI(lifespan=lifespan)
    app.add_middleware(SocialPreviewMiddleware)

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
