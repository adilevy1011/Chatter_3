from socket_client import sio

from handle_ai import start_new_ai_chat, send_ai_message, get_ai_chats

import flet as ft

from route_handling import route_change

@sio.event
def connect():
    print("Successfully connected!")


@sio.event
def disconnect():
    print("Disconnected from server")

@sio.on('reply')
def on_reply(data):
    print(data)



# Building app views



def main(page: ft.Page):
    page.on_route_change = route_change
    page.route = "/login"
    route_change(page=page)


if __name__ == '__main__':
    sio.connect('http://127.0.0.1:5678')
    while not sio.connected:
         sio.sleep(0.1)
    ft.run(main=main,assets_dir='assets')

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
