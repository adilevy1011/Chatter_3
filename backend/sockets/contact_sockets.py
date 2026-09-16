from backend.config import sio
from backend.services.supabase.handle_contacts import add_user_contact, get_user_contacts

def register_contact_sockets():

    @sio.on('add_contact')
    def add_contact(data):
        return add_user_contact(data['contact_id'])

    @sio.on('get_contacts')
    def get_contacts(data):
        return get_user_contacts()