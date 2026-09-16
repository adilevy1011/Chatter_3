import flet as ft
from frontend.handle_ai import get_chat_messages, get_ai_chats, send_ai_message
from frontend.branding import WINDOW_ICON
from datetime import datetime
import asyncio

class TypingIndicator(ft.Row):
    def __init__(self):
        super().__init__()
        self.visible = False
        self.spacing = 4
        self.vertical_alignment = ft.CrossAxisAlignment.CENTER
        
        self.dot1 = self._create_dot()
        self.dot2 = self._create_dot()
        self.dot3 = self._create_dot()
        
        self.controls = [self.dot1, self.dot2, self.dot3]
        self._running = False
    def change_visible(self):
        self.visible = not self.visible
    def _create_dot(self):
        return ft.Container(
            width=8,
            height=8,
            bgcolor=ft.Colors.GREY_400,
            border_radius=4,
            offset=ft.Offset(0, 0),
            animate_offset=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
        )

    def did_mount(self):
        self._running = True
        self.page.run_task(self._animate_dots)

    def will_unmount(self):
        self._running = False

    async def _animate_dots(self):
        # Staggered jumping loop
        while self._running:
            try:
                # Dot 1 jumps up
                self.dot1.offset = ft.Offset(0, -0.6)
                self.dot1.update()
                await asyncio.sleep(150 / 1000)

                # Dot 1 down, Dot 2 up
                self.dot1.offset = ft.Offset(0, 0)
                self.dot2.offset = ft.Offset(0, -0.6)
                self.dot1.update()
                self.dot2.update()
                await asyncio.sleep(150 / 1000)

                # Dot 2 down, Dot 3 up
                self.dot2.offset = ft.Offset(0, 0)
                self.dot3.offset = ft.Offset(0, -0.6)
                self.dot2.update()
                self.dot3.update()
                await asyncio.sleep(150 / 1000)

                # Dot 3 down
                self.dot3.offset = ft.Offset(0, 0)
                self.dot3.update()
                await asyncio.sleep(150 / 1000)
            except RuntimeError as error:
                if "destroyed session" not in str(error).lower():
                    raise
                self._running = False

async def build_chat_view(page: ft.Page, thread_id: str) -> ft.View:
    page.title = "Chatter"

    page.window.icon = WINDOW_ICON

    async def get_chat_title():
        ai_chats = await get_ai_chats()
        for chat in ai_chats:
            if chat['id'] == thread_id:
                return chat['thread_title']

    def get_formatted_timestamp(timestamp):
        #2026-09-06 19:21:23.584143+00
    
        dt_utc = datetime.fromisoformat(timestamp)
        dt_local = dt_utc.astimezone(None)
        readable_date = dt_local.strftime("%B %d, %Y at %I:%M %p")

        return readable_date


    thinking_dropdown = ft.Dropdown(
        value="Fast", # Default option
        width=140,
        hint_text="Model",
        border=ft.InputBorder.NONE,
        options=[
            ft.dropdown.Option("Fast"),
            ft.dropdown.Option("Thinking"),
        ],
    )
    messageBox = ft.TextField(hint_text="Type your message here...", width=1000)
    input_bar = ft.Container(
        content=ft.Row(
            controls=[
                messageBox,
                ft.VerticalDivider(width=1),
                thinking_dropdown,
            ],
            spacing=0,
        ),
        border_radius=8,
    )
    send_button = ft.Button(
        content="Send",
        on_click=lambda _: page.run_task(
            send_message, messageBox.value, thinking_dropdown.value
        ),
    )
    typing_indicator = TypingIndicator()

    async def update_if_active() -> bool:
        if page.route != f"/chat/{thread_id}":
            return False
        try:
            page.update()
        except RuntimeError as error:
            if "destroyed session" not in str(error).lower():
                raise
            return False
        return True

    async def send_message(content,thinking):
        if not content:
            return
        messageBox.value = ""
        timestamp = datetime.now().astimezone().strftime("%B %d, %Y at %I:%M %p")
        messages.controls.append(
            message_bubble(
                content,
                timestamp,
                ft.MainAxisAlignment.END,
                ft.Colors.PRIMARY_CONTAINER,
            )
        )
        typing_indicator.change_visible()
        try:
            if not await update_if_active():
                return
            response = await send_ai_message(content, thread_id, thinking)
            if page.route != f"/chat/{thread_id}":
                return
            updated_title = await get_chat_title()
            if updated_title:
                chat_title.value = updated_title
            messages.controls.append(
                message_bubble(
                    response.get("response", ""),
                    timestamp,
                    ft.MainAxisAlignment.START,
                    ft.Colors.SURFACE_CONTAINER_HIGHEST,
                    response.get("thinking", ""),
                )
            )
            await update_if_active()
        finally:
            typing_indicator.change_visible()
            await update_if_active()
    message_controls = ft.Row(
         controls=[input_bar,send_button],
         spacing=20,
         
    )

    async def get_messages():
        messages = await get_chat_messages(thread_id)
        if messages is None:
              messages = []
        return messages

    def message_bubble(content, timestamp, alignment, color, thinking=""):
        assistant_content = []
        if thinking:
            assistant_content.append(
                ft.ExpansionTile(
                    title=ft.Text("Thinking", size=12),
                    controls=[
                        ft.Markdown(
                            value=thinking,
                            selectable=True,
                            extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                            code_theme="atom-one-dark",
                        )
                    ],
                )
            )
        assistant_content.append(
            ft.Markdown(
                value=content,
                selectable=True,
                extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                code_theme="atom-one-dark",
            )
        )
        return ft.Row(
            controls=[
                ft.Container(
                    content=ft.Column(
                        controls=[
                            *assistant_content,
                            ft.Text(
                                value=timestamp,  
                                size=10,
                                color=ft.Colors.WHITE54,
                            ),
                        ],
                        tight=True, 
                        horizontal_alignment=ft.CrossAxisAlignment.START, 
                        spacing=2,
                        width=550,
                    ),
                    bgcolor=color,
                    padding=10,
                    border_radius=10,
                )
            ],
            
            alignment=alignment,
        )

    def build_message_items(user_message, assistant_message, timestamp, thinking=""):
        return [
            message_bubble(
                user_message,
                timestamp,
                ft.MainAxisAlignment.END,
                ft.Colors.PRIMARY_CONTAINER,
            ),
            message_bubble(
                assistant_message,
                timestamp,
                ft.MainAxisAlignment.START,
                ft.Colors.SURFACE_CONTAINER_HIGHEST,
                thinking,
            ),
        ]

    async def build_messages_items():
        items = []
        for message in await get_messages():
            timestamp = message['created_at']
            assistant_message = message["assistant_message"]
            if isinstance(assistant_message, dict):
                assistant_message = assistant_message.get("response", "")
            thinking = message.get("ai_thinking", "")
            if not isinstance(thinking, str) or thinking == "Fast":
                thinking = ""
            items.extend(
                build_message_items(
                    message["user_message"],
                    assistant_message,
                    get_formatted_timestamp(timestamp),
                    thinking,
                )
            )
        return items
    async def back_to_chats(e):
        await page.push_route('/')

    chat_title = ft.Text(
        value=await get_chat_title(),
        weight=ft.FontWeight.BOLD,
        size=27,
    )

    messages = ft.ListView(
            controls=await build_messages_items(),
            expand=True,
            spacing=5,
            padding=10,
            scroll=ft.ScrollMode.AUTO,
        )
    return ft.View(
        route="/chat",
        appbar=ft.AppBar(
            title=chat_title,
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            actions=[
                ft.Button('Back to chats',on_click=back_to_chats)
            ]
        ),
        controls=[
            ft.Text("", style=ft.TextStyle(size=20, weight=ft.FontWeight.BOLD)),
            messages,
            typing_indicator,
            message_controls,
            
        ],
    )
