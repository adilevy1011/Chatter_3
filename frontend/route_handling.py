from login import build_login_view
from main_app import build_main_view
from chat_view import build_chat_view
import flet as ft
from urllib.parse import unquote


async def navigate_to_main(page: ft.Page):
    page.route = "/"
    await page.push_route("/")
    route_change(page=page)


def route_change(e: ft.RouteChangeEvent | None = None, page: ft.Page | None = None):
    if e is not None:
        page = e.page
    if page is None:
        raise RuntimeError("A page is required to handle a route change")
    page.views.clear()

    if page.route == "/":
        page.views.append(build_main_view(page))
    elif page.route.startswith("/chat/"):
        thread_id = unquote(page.route.removeprefix("/chat/"))
        if not thread_id:
            raise RuntimeError("A thread ID is required to open a chat")
        page.views.append(build_chat_view(page, thread_id))
    else:
        page.views.append(
            build_login_view(
                page, on_authenticated=lambda: navigate_to_main(page)
            )
        )

    page.update()