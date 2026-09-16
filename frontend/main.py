# frontend_main.py
from frontend.socket_client import sio
import flet as ft
from frontend.route_handling import route_change

@sio.event
def connect():
    print("Successfully connected to WebSocket backend!")

@sio.event
def disconnect():
    print("Disconnected from server")

async def main(page: ft.Page):
    
    if not sio.connected:
        try:
            await sio.connect('https://new.chatter-2.com', transports=['websocket'])
        except Exception as e:
            print(f"Socket connection error: {e}")

    page.on_route_change = route_change
    page.route = "/login"
  
    route_change(page=page)
