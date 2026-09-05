import flet as ft
from auth import signup, login
from collections.abc import Awaitable, Callable


def build_login_view(
    page: ft.Page, on_authenticated: Callable[[], Awaitable[None]]
) -> ft.View:
    
    page.title = "Chatter - login"
    page.window.icon = "chatter-icon2.ico"
    
    #username_input = ft.TextField(label="username", width=300)
    login_header = ft.Text("Log into your Chatter account")
    email_input = ft.TextField(label="Email", width=300)
    password_input = ft.TextField(label="Password",width=300,password=True,can_reveal_password=True,)
    
    confirmation_text = ft.Text('')
    signup_mode = False

    async def login_button_clicked(e):
        if not email_input.value or not password_input.value:
            confirmation_text.value = "One or more fields are missing"
            page.update()
        else:
            
            email_input.error_text = None
            login_response = login(email_input.value,password_input.value)
            if isinstance(login_response, dict) and login_response.get('success'):
                confirmation_text.value = 'Login successful. Taking you there...'
                await on_authenticated()
                
            else:
                confirmation_text.value = (
                    login_response.get('error')
                    if isinstance(login_response, dict)
                    else str(login_response)
                )
                page.update()
    async def signup_button_clicked(e):
            if not email_input.value or not password_input.value:
                confirmation_text.value = "One or more fields are missing"
                page.update()
            else:
                
                email_input.error_text = None
                signup_response = signup(email_input.value,password_input.value)
                if isinstance(signup_response, dict) and signup_response.get('success'):
                    confirmation_text.value = 'Account created. Taking you there...'
                    await on_authenticated()
                    
                else:
                    confirmation_text.value = (
                        signup_response.get('error')
                        if isinstance(signup_response, dict)
                        else str(signup_response)
                    )
                    page.update()
    async def toggle_signup_login(e):
        nonlocal signup_mode
        signup_mode = not signup_mode
        if signup_mode:
            login_header.value = 'Create a Chatter account'
        else:
            login_header.value = 'Log into your Chatter account'
        submit_login_button.visible = not submit_login_button.visible
        submit_signup_button.visible = not submit_signup_button.visible
        if signup_mode:
            toggle_button.content = "Already have an account? Sign in"
        else:
            toggle_button.content = "Don't have an account? Sign up"
        page.update()

    submit_login_button = ft.Button("Login", on_click=login_button_clicked)
    submit_signup_button = ft.Button("Create account", on_click=signup_button_clicked,visible=False)
    toggle_button = ft.Button("Don't have an account? Sign up", on_click=toggle_signup_login)
    return ft.View(
        route = "/login",
        appbar = ft.AppBar(
            title=ft.Text(
                value="Welcome to Chatter", 
                weight=ft.FontWeight.BOLD, 
                size=27
            ),
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        ),
        controls=[
            login_header,
            email_input,
            password_input,
            confirmation_text,
            submit_login_button,
            submit_signup_button,
            toggle_button,

        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )