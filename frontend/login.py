import flet as ft
from frontend.auth import signup, login, login_with_token
from collections.abc import Awaitable, Callable
import json

TOKEN_KEY = "com.chatter-2.session"


async def save_token(
    preferences: ft.SharedPreferences, tokens: dict[str, str]
):
    await preferences.set(TOKEN_KEY, json.dumps(tokens))


async def load_token(
    preferences: ft.SharedPreferences,
) -> dict[str, str] | None:
    try:
        value = await preferences.get(TOKEN_KEY)
        if not isinstance(value, str):
            return None
        data = json.loads(value)
        if data.get("access_token") and data.get("refresh_token"):
            return data
    except (TypeError, ValueError, json.JSONDecodeError):
        return None
    return None


async def clear_token(preferences: ft.SharedPreferences):
    await preferences.remove(TOKEN_KEY)


class SessionRestorer(ft.Container):
    def __init__(self, restore: Callable[[], Awaitable[None]]):
        super().__init__(width=0, height=0)
        self._restore = restore

    def did_mount(self):
        self.page.run_task(self._restore)


def build_login_view(
    page: ft.Page, on_authenticated: Callable[[], Awaitable[None]]
) -> ft.View:
    preferences = ft.SharedPreferences()

    page.title = "Chatter - login"
    page.window.icon = "chatter-icon2.ico"
    
    username_input = ft.TextField(label="username", width=300, visible=False)
    login_header = ft.Text("Log into your Chatter account")
    email_input = ft.TextField(label="Email", width=300)
    password_input = ft.TextField(label="Password", width=300, password=True, can_reveal_password=True)
    
    confirmation_text = ft.Text('')
    signup_mode = False

    async def finish_authentication(message: str):
        confirmation_text.color = ft.Colors.GREEN
        confirmation_text.value = message
        page.update()
        try:
            await on_authenticated()
        except Exception as error:
            confirmation_text.color = ft.Colors.RED
            confirmation_text.value = f"Could not open Chatter: {error}"
            page.update()

    async def check_auto_login():
        stored_tokens = await load_token(preferences)
        if stored_tokens:
            confirmation_text.color = ft.Colors.BLUE
            confirmation_text.value = "Restoring session..."
            page.update()
            
            token_response = await login_with_token(
                stored_tokens["access_token"],
                stored_tokens["refresh_token"],
            )
            if isinstance(token_response, dict) and token_response.get("success"):
                if (
                    token_response.get("access_token")
                    and token_response.get("refresh_token")
                ):
                    await save_token(
                        preferences,
                        {
                            "access_token": token_response["access_token"],
                            "refresh_token": token_response["refresh_token"],
                        },
                    )
                await finish_authentication("Session restored! Redirecting...")
            else:
                await clear_token(preferences)
                confirmation_text.color = ft.Colors.RED
                confirmation_text.value = (
                    token_response.get("error", "Saved session has expired")
                    if isinstance(token_response, dict)
                    else str(token_response)
                )
                page.update()

    session_restorer = SessionRestorer(check_auto_login)

    async def login_button_clicked(e):
        if not email_input.value or not password_input.value:
            confirmation_text.color = ft.Colors.RED
            confirmation_text.value = "One or more fields are missing"
            page.update()
        else:
            email_input.error_text = None
            login_response = await login(email_input.value, password_input.value)
            if isinstance(login_response, dict) and login_response.get('success'):
                if login_response.get('access_token') and login_response.get('refresh_token'):
                    await save_token(
                        preferences,
                        {
                            "access_token": login_response["access_token"],
                            "refresh_token": login_response["refresh_token"],
                        },
                    )
                
                await finish_authentication(
                    'Login successful. Taking you there...'
                )
            else:
                confirmation_text.color = ft.Colors.RED
                confirmation_text.value = (
                    login_response.get('error')
                    if isinstance(login_response, dict)
                    else str(login_response)
                )
                page.update()

    async def signup_button_clicked(e):
        if not email_input.value or not password_input.value or not username_input.value:
            confirmation_text.value = "One or more fields are missing"
            page.update()
        else:
            email_input.error_text = None
            signup_response = await signup(
                email_input.value,
                password_input.value,
                username_input.value,
            )
            if isinstance(signup_response, dict) and signup_response.get('success'):
                if signup_response.get('access_token') and signup_response.get('refresh_token'):
                    await save_token(
                        preferences,
                        {
                            "access_token": signup_response["access_token"],
                            "refresh_token": signup_response["refresh_token"],
                        },
                    )

                await finish_authentication(
                    'Account created. Taking you there...'
                )
            else:
                confirmation_text.color = ft.Colors.RED
                confirmation_text.value = (
                    signup_response.get('error')
                    if isinstance(signup_response, dict)
                    else str(signup_response)
                )
                page.update()

    async def toggle_signup_login(e):
        nonlocal signup_mode
        signup_mode = not signup_mode
        login_header.value = 'Create a Chatter account' if signup_mode else 'Log into your Chatter account'
        submit_login_button.visible = not submit_login_button.visible
        submit_signup_button.visible = not submit_signup_button.visible
        username_input.visible = not username_input.visible
        toggle_button.content = "Sign in" if signup_mode else "Create account"
        page.update()

    submit_login_button = ft.Button("Login", on_click=login_button_clicked)
    submit_signup_button = ft.Button("Create account", on_click=signup_button_clicked, visible=False)
    toggle_button = ft.Button("Create account", width=125, height=30, style=ft.ButtonStyle(text_style=ft.TextStyle(size=11)), on_click=toggle_signup_login)
    
    return ft.View(
        route="/login",
        appbar=ft.AppBar(
            title=ft.Text(value="Welcome to Chatter", weight=ft.FontWeight.BOLD, size=27),
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        ),
        controls=[
            login_header,
            email_input,
            username_input,
            password_input,
            confirmation_text,
            submit_login_button,
            submit_signup_button,
            toggle_button,
            session_restorer,
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
