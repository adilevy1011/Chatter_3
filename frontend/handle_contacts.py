from frontend.socket_client import ensure_connected, sio

async def add_contact(contact_id):
    await ensure_connected()
    return await sio.call(
        'add_contact', {'contact_id': contact_id}, namespace='/'
    )

async def get_contacts():
    await ensure_connected()
    return await sio.call('get_contacts', namespace='/')
