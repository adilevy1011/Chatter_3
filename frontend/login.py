import flet as ft
from auth import signup, login, login_with_token
from collections.abc import Awaitable, Callable
import json
from pathlib import Path

TOKEN_FILE = Path.home() / ".chatter_session.json"

def save_token(token: str):
    TOKEN_FILE.write_text(json.dumps({"auth_token": token}))

def load_token() -> str | None:
    if TOKEN_FILE.exists():
        try:
            data = json.loads(TOKEN_FILE.read_text())
            return data.get("auth_token")
        except Exception:
            return None
    return None

def clear_token():
    if TOKEN_FILE.exists():
        TOKEN_FILE.unlink()


def build_login_view(
    page: ft.Page, on_authenticated: Callable[[], Awaitable[None]]
) -> ft.View:
    
    page.title = "Chatter - login"
    page.window.icon = "chatter-icon2.ico"
    
    username_input = ft.TextField(label="username", width=300, visible=False)
    login_header = ft.Text("Log into your Chatter account")
    email_input = ft.TextField(label="Email", width=300)
    password_input = ft.TextField(label="Password", width=300, password=True, can_reveal_password=True)
    
    confirmation_text = ft.Text('')
    signup_mode = False

    async def check_auto_login():
        stored_token = load_token()
        if stored_token:
            confirmation_text.color = ft.Colors.BLUE
            confirmation_text.value = "Restoring session..."
            page.update()
            
            token_response = login_with_token(stored_token)
            if isinstance(token_response, dict) and token_response.get('success'):
                confirmation_text.color = ft.Colors.GREEN
                confirmation_text.value = "Session restored! Redirecting..."
                page.update()
                await on_authenticated()
            else:
                clear_token()
                confirmation_text.value = ""
                page.update()

    page.run_task(check_auto_login)

    async def login_button_clicked(e):
        if not email_input.value or not password_input.value:
            confirmation_text.color = ft.Colors.RED
            confirmation_text.value = "One or more fields are missing"
            page.update()
        else:
            email_input.error_text = None
            login_response = login(email_input.value, password_input.value)
            if isinstance(login_response, dict) and login_response.get('success'):
                if 'token' in login_response and login_response['token']:
                    save_token(login_response['token'])
                
                confirmation_text.color = ft.Colors.GREEN
                confirmation_text.value = 'Login successful. Taking you there...'
                page.update()
                await on_authenticated()
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
            signup_response = signup(email_input.value, password_input.value, username_input.value)
            if isinstance(signup_response, dict) and signup_response.get('success'):
                if 'token' in signup_response and signup_response['token']:
                    save_token(signup_response['token'])

                confirmation_text.color = ft.Colors.GREEN
                confirmation_text.value = 'Account created. Taking you there...'
                page.update()
                await on_authenticated()
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
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )