import flet as ft
from handle_ai import get_ai_chats,start_new_ai_chat
from auth import logout, get_profile
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
    def get_username():
        profile_list = get_profile()
        username = profile_list['username']
        return username
    def get_email():
        profile_list = get_profile()
        email = profile_list['email']
        return email
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
    
    profile_card = ft.Card(
        elevation =5,
        content=ft.Container(
            content=ft.Column(
                [
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.ALBUM, color=ft.Colors.BLUE),
                        title=ft.Text("Profile"),
                    ),
                    ft.Text(f"Username: {get_username()}"),
                    ft.Text(f'Email: {get_email()}'),
                    ft.Row(
                        [
                            ft.TextButton("Close", on_click=lambda _: close_profile_card()),
                        ],
                        alignment=ft.MainAxisAlignment.END,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                tight=True,
            ),
            padding=15,
            width=350,
        ),

    )
    profile_popup = ft.AlertDialog(
        content=profile_card,
        content_padding=0,  # Removes default padding so the card fills the border tightly
    )
    def open_profile_card(e):
        page.show_dialog(profile_popup)

    def close_profile_card():
        page.pop_dialog()

    new_chat_button = ft.Button("Start a new chat",on_click=new_chat)
    return ft.View(
        route="/",
        appbar=ft.AppBar(
            title=ft.Text(value="Chatter", weight=ft.FontWeight.BOLD, size=27),
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            actions=[
                ft.PopupMenuButton(
                    items=[
                        ft.PopupMenuItem(content="Profile",on_click=open_profile_card),
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
