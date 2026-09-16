from frontend.socket_client import sio
import flet as ft
from frontend.route_handling import route_change

@sio.event
def connect():
    print("Successfully connected!")

@sio.event
def disconnect():
    print("Disconnected from server")

if not sio.connected:
    sio.connect('https://chatter-2.com', transports=['websocket'])

async def main(page: ft.Page):
    if not sio.connected:
        await sio.wait() 

    page.on_route_change = route_change
    page.route = "/login"
    route_change(page=page)

if __name__ == '__main__':
    sio.connect('https://chatter-2.com',transports=['websocket']) #147.182.235.138
    while not sio.connected:
         sio.sleep(0.1)
    #ft.run(main=main,assets_dir='assets',view=ft.AppView.WEB_BROWSER)