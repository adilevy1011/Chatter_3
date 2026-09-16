from socket_client import sio
import flet as ft
from route_handling import route_change

@sio.event
def connect():
    print("Successfully connected!")

@sio.event
def disconnect():
    print("Disconnected from server")

def main(page: ft.Page):
    page.on_route_change = route_change
    page.route = "/login"
    route_change(page=page)

if __name__ == '__main__':
    sio.connect('http://147.182.235.138',transports=['websocket']) #147.182.235.138
    while not sio.connected:
         sio.sleep(0.1)
    #ft.run(main=main,assets_dir='assets',view=ft.AppView.WEB_BROWSER)