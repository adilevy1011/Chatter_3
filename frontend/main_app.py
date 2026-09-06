import flet as ft
from handle_ai import get_ai_chats,start_new_ai_chat
from auth import logout
from login import clear_token
def build_main_view(page: ft.Page) -> ft.View:
    page.title = "Chatter"
    page.window.icon = "chatter-icon2.ico"

    def build_chat_items():
        return [
            ft.ListTile(
                leading=ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=40),
                title=ft.Text(thread["thread_title"]),
                subtitle=ft.Text("Last message snippet goes here..."),
                on_click=chat_clicked,
                hover_color=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            )
            for thread in get_ai_chats()
        ]

    def new_chat(e):
        start_new_ai_chat('new chat')
        chat_list.controls = build_chat_items()
        page.update()

    def chat_clicked(e):
        print(f"Selected chat: {e.control.data}")

    async def logout_clicked(e):
        logout()
        clear_token()
        await page.push_route("/login")

    chat_list = ft.ListView(
        controls=build_chat_items(),
        expand=True,
        spacing=5,
        padding=10,
        scroll=ft.ScrollMode.AUTO,  
    )

    new_chat_button = ft.Button("Start a new chat",on_click=new_chat)
    return ft.View(
        route="/",
        appbar=ft.AppBar(
            title=ft.Text(value="Chatter", weight=ft.FontWeight.BOLD, size=27),
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            actions=[
                ft.PopupMenuButton(
                    items=[
                        ft.PopupMenuItem(content="Profile"),
                        ft.PopupMenuItem(content="Logout", on_click=logout_clicked),
                    ]
                ),
            ],
        ),
        controls=[
            ft.Text("Messages", style=ft.TextStyle(size=20, weight=ft.FontWeight.BOLD)),
            new_chat_button,
            chat_list,
            
            
        ],
    )
