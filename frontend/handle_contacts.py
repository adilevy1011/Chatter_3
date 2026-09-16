from socket_client import sio

def add_contact(contact_id):
    sio.call('add_contact',{'contact_id':contact_id})

def get_contacts():
    sio.call('get_contacts')