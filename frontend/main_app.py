import flet as ft

def build_main_view(page: ft.Page) -> ft.View:
    page.title = "Chatter"
    page.window.icon = "chatter-icon2.ico"
    text = ft.Text('Chatter coming soon')

    return ft.View(
        route="/",
        controls=[
            text
        ],
    )

