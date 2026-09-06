import flet as ft
from handle_ai import get_chat_messages, get_ai_chats, send_ai_message

def build_chat_view(page: ft.Page, thread_id: str) -> ft.View:
    page.title = "Chatter"

    page.window.icon = "chatter-icon2.ico"

    def get_chat_title():
        ai_chats = get_ai_chats()
        for chat in ai_chats:
            if chat['id'] == thread_id:
                return chat['thread_title']

    
    messageBox = ft.TextField(hint_text="Type your message here...", width=1000)
    send_button =ft.Button(content="Send",on_click=lambda e: send_message(messageBox.value))
    def send_message(content):
        if not content:
            return

        response = send_ai_message(content, thread_id)
        messages.controls.extend(build_message_items(content, response))
        messageBox.value = ""
        page.update()

    message_controls = ft.Row(
         controls=[messageBox,send_button],
         spacing=20,
         
    )

    def get_messages():
        messages = get_chat_messages(thread_id)
        if messages is None:
              messages = []
        return messages

    def message_bubble(content, alignment, color):
        return ft.Row(
            controls=[
                ft.Container(
                    content=ft.Markdown(
                    value=content,
                    selectable=True,
                    extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                    code_theme="atom-one-dark",
                    ),
                    bgcolor=color,
                    padding=10,
                    border_radius=10,
                )
            ],
            alignment=alignment,
        )

    def build_message_items(user_message, assistant_message):
        return [
            message_bubble(
                user_message,
                ft.MainAxisAlignment.START,
                ft.Colors.SURFACE_CONTAINER_HIGHEST,
            ),
            message_bubble(
                assistant_message,
                ft.MainAxisAlignment.END,
                ft.Colors.PRIMARY_CONTAINER,
            ),
        ]

    def build_messages_items():
        items = []
        for message in get_messages():
            items.extend(
                build_message_items(
                    message["user_message"],
                    message["assistant_message"],
                )
            )
        return items


    messages = ft.ListView(
            controls=build_messages_items(),
            expand=True,
            spacing=5,
            padding=10,
            scroll=ft.ScrollMode.AUTO,
        )
    return ft.View(
        route="/chat",
        appbar=ft.AppBar(
            title=ft.Text(value=get_chat_title(), weight=ft.FontWeight.BOLD, size=27),
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        ),
        controls=[
            ft.Text("", style=ft.TextStyle(size=20, weight=ft.FontWeight.BOLD)),
            messages,
            message_controls
        ],
    )