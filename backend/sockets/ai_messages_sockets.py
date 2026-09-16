from backend.services.ai_service import generate_claude_message, generate_chat_title
from backend.services.supabase.ai import fetch_ai_chats, fetch_chat_messages, make_new_ai_chat, send_ai_message, rename_ai_chat
from backend.config import sio

def register_ai_messages_sockets():

    @sio.on('fetch_messages')
    async def get_messages(sid, data):
        return fetch_chat_messages(data['thread_id'])

    @sio.on('fetch_ai_chats')
    async def get_ai_chats(sid):
        return fetch_ai_chats()

    @sio.on('send_ai_message')
    async def send_message(sid, data):
        new_chat = True
        messages_list = fetch_chat_messages(data['thread_id'])
        messages = []
        for message_with_ai in messages_list:
            messages.append({
                'role':'user',
                'content':message_with_ai['user_message']
            })
            messages.append({
                'role':'assistant',
                'content':message_with_ai['assistant_message']
            })
        if messages:
            new_chat = False
        messages.append({
            'role':'user',
            'content':data['message']
        })
        if new_chat:
            new_title = generate_chat_title(messages=messages)
            rename_ai_chat(data['thread_id'],new_title)
        thinking_enabled = data["thinking"] == "Thinking"
        response = generate_claude_message(messages, thinking_enabled)
        send_ai_message(
            thread_id=data['thread_id'],
            user_message=data['message'],
            ai_response=response["response"],
            thinking=response.get("thinking", ""),
        )
        return response
    @sio.on('start_new_chat')
    async def start_new_ai_chat(sid, data):
        return make_new_ai_chat(data['title'])