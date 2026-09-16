from frontend.socket_client import ensure_connected, sio

async def send_ai_message(message, thread_id, thinking):
    await ensure_connected()
    return await sio.call(
        'send_ai_message',
        {'message': message, 'thread_id': thread_id, 'thinking': thinking},
        namespace='/',
    )

async def start_new_ai_chat(title):
    await ensure_connected()
    return await sio.call('start_new_chat', {'title': title}, namespace='/')

async def get_ai_chats():
    await ensure_connected()
    return await sio.call('fetch_ai_chats', namespace='/')

async def get_chat_messages(thread_id):
    await ensure_connected()
    return await sio.call(
        'fetch_messages', {'thread_id': thread_id}, namespace='/'
    )
