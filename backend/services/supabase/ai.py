from . import supabase

def fetch_ai_chats():
    session = supabase.auth.get_session()
    if session:
        user_id = session.user.id
        response = (
            supabase.table("ai_chat_threads")
            .select("*")
            .eq("user_id", user_id)
            .execute()
        )
        return response.data
def fetch_chat_messages(thread_id):
    response = (
        supabase.table("ai_chat_messages")
        .select("*")
        .eq("thread_id",thread_id)
        .execute()
    )
    return response.data
def make_new_ai_chat(thread_title):
    session = supabase.auth.get_session()
    if session:
        user_id = session.user.id
        response = (
                supabase.table('ai_chat_threads')
                .insert({'user_id':user_id,'thread_title':thread_title}).execute()
            )
        return response.data
    else:
        raise Exception("Could not verify valid session")

def rename_ai_chat(thread_id,title):
    response = (
        supabase.table('ai_chat_threads')
        .update({'thread_title':title})
        .eq("id",thread_id)
        .execute()
        
    )
    return response.data


def send_ai_message(thread_id,user_message,ai_response,thinking):
    session = supabase.auth.get_session()
    if session:
        user_id = session.user.id
        response = (
            supabase.table('ai_chat_messages')
            .insert({'thread_id':thread_id,'user_id':user_id,
                        'user_message':user_message,'assistant_message':ai_response,'ai_thinking':thinking}).execute()
        )
        return response.data
    else:
        raise Exception("Could not verify valid session")
    
    
    