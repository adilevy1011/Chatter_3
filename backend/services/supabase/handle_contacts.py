from . import supabase

def get_user_contacts():
    session = supabase.auth.get_session()
    if session:
        user_id = session.user.id
        response = (
            supabase.table('contacts')
            .select('*')
            .eq('user_id',user_id)
            .execute()
        )
        return response.data
    else:
        raise Exception("Could not verify valid session")

def add_user_contact(contact_id):
    session = supabase.auth.get_session()
    if session:
        user_id = session.user.id
        response = (
            supabase.table('contacts')
            .insert({'user_id':user_id,'contact_id':contact_id})
            .execute()
        )
        return response.data
    else:
        raise Exception("Could not verify valid session")