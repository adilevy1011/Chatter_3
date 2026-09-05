from socket_client import sio

from auth import signup, login
from handle_ai import start_new_ai_chat, send_ai_message, get_ai_chats

import flet as ft


@sio.event
def connect():
    print("Successfully connected!")


@sio.event
def disconnect():
    print("Disconnected from server")

@sio.on('reply')
def on_reply(data):
    print(data)

def route_change(e: ft.RouteChangeEvent | None = None, page: ft.Page | None = None):
    if e is not None:
        page = e.page
    if page is None:
        raise RuntimeError("A page is required to handle a route change")
    page.views.clear()

    if page.route == "/main":
        page.views.append(build_main_view(page))
    else:
        page.views.append(build_login_view(page))

    page.update()

# Building app views

def build_main_view(page: ft.Page) -> ft.View:
    page.title = "Chatter"
    
    text = ft.Text('Chatter coming soon')

    return ft.View(
        route="/main",
        controls=[
            text
        ],
    )

def build_login_view(page: ft.Page) -> ft.View:
    page.title = "Chatter - login"
    email_input = ft.TextField(label="Email", width=300)
    password_input = ft.TextField(label="Password",width=300)
    confirmation_text = ft.Text('')
    async def login_button_clicked(e):
        if not email_input.value or not password_input.value:
            confirmation_text.value = "One or more fields are missing"
            page.update()
        else:
            
            email_input.error_text = None
            login_response = login(email_input.value,password_input.value)
            if login_response.get('success'):
                confirmation_text.value = 'Login successful. Taking you there...'
                page.update()
                await page.push_route('/main')
                
            else:
                confirmation_text.value = login_response.get('error')
                page.update()
    submit_login_button = ft.Button("Login", on_click=login_button_clicked)

    return ft.View(
        route = "/",
        controls=[
            email_input,
            password_input,
            confirmation_text,
            submit_login_button
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

def main(page: ft.Page):
    page.on_route_change = route_change
    route_change(page=page)


if __name__ == '__main__':
    sio.connect('http://127.0.0.1:5678')
    while not sio.connected:
         sio.sleep(0.1)
    ft.run(main=main)

    # 
    #
    # have_account = input("Have an account? ")
    
    # email = input('Email: ')
    # password = input('password: ')

    # if have_account == 'yes':
    #     login(email,password)
    # else:
    #     signup(email,password)
    # ai_chats = get_ai_chats()
    # if ai_chats:
    #     for chat in ai_chats:
    #         print(chat['thread_title'])
    # else:
    #     make_chat = input('no chats yet, make one?(y,n) ')
    #     if make_chat == 'y':
    #         title = input('title')
    #         start_new_ai_chat(title)
    #message = input('Type your message: ')
    # while message != 'stop':
    #     response = send_ai_message(message)
    #     print(response)
    #     message = input('Type your message: ')
