from login import build_login_view
from main_app import build_main_view

import flet as ft


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
    else:
        page.views.append(
            build_login_view(
                page, on_authenticated=lambda: navigate_to_main(page)
            )
        )

    page.update()