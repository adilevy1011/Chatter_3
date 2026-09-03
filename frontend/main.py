import socketio

sio = socketio.Client()

@sio.event
def connect():
    print("Successfully connected!")

@sio.event
def disconnect():
    print("Disconnected from server")

@sio.on('reply')
def on_reply(data):
    print(data)

def send_ai_message(message):
    return sio.call('ai_message',message)

if __name__ == '__main__':
    sio.connect('http://127.0.0.1:5678')
    while not sio.connected:
        sio.sleep(0.1)
    message = input('type in your message here: ')
    while message != 'stop':
        response = send_ai_message(message)
        print(response)
        sio.sleep(0.3)
        message = input('type in your message here: ')
