from socket_client import sio

def send_ai_message(message,thread_id):
    return sio.call('send_ai_message',{'message':message,'thread_id':thread_id})

def start_new_ai_chat(title):
    return sio.call('start_new_chat', {'title': title})

def get_ai_chats():
    return sio.call('fetch_ai_chats')

def get_chat_messages(thread_id):
    return sio.call('fetch_messages',{'thread_id':thread_id})
