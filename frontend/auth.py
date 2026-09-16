
from frontend.socket_client import ensure_connected, sio

async def login(email, password):
    try:
        await ensure_connected()
        response = await sio.call(
            'login',
            {'email': email, 'password': password},
            namespace='/',
            timeout=15,
        )
        print("Server response:", response)
        return response
    except Exception as e:
        return f"Login failed: {str(e)}"

async def login_with_token(access_token, refresh_token):
    try:
        await ensure_connected()
        response = await sio.call(
            'login_with_token',
            {'access_token': access_token, 'refresh_token': refresh_token},
            namespace='/',
            timeout=15,
        )
        print("Token server response:", response)
        return response
    except Exception as e:
        return f"Token login failed: {str(e)}"
    
async def signup(email, password, username, full_name=None, avatar_url=None):
    try:
        await ensure_connected()
        response = await sio.call(
            'signup',
            {
                'email': email,
                'password': password,
                'username': username,
                'full_name': full_name,
                'avatar_url': avatar_url,
            },
            namespace='/',
            timeout=15,
        )
        print("Server response:", response)
        return response
    except Exception as e:
        return f"signup failed: {str(e)}"

async def get_profile():
    try:
        await ensure_connected()
        response = await sio.call('fetch_user_profile', namespace='/')
        return response
    except Exception as e:
        return f"Could not get fetch profile details: {str(e)}"

async def logout():
    try:
        await ensure_connected()
        response = await sio.call('signout', namespace='/')
        return response
    except Exception as e:
        return f"Logout failed: {str(e)}"
