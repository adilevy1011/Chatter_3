
from frontend.socket_client import sio

def login(email,password):
    try:
        response = sio.call('login',{'email': email, 'password': password},timeout=15)
        print("Server response:", response)
        return response
    except Exception as e:
        return f"Login failed: {str(e)}"

def login_with_token(access_token, refresh_token):
    try:
        response = sio.call(
            'login_with_token',
            {'access_token': access_token, 'refresh_token': refresh_token},
            timeout=15,
        )
        print("Token server response:", response)
        return response
    except Exception as e:
        return f"Token login failed: {str(e)}"
    
def signup(email,password,username,full_name=None,avatar_url=None):
    try:
        response = sio.call('signup',{'email': email, 'password': password,'username':username,'full_name':full_name,'avatar_url':avatar_url},timeout=15)
        print("Server response:", response)
        return response
    except Exception as e:
        return f"signup failed: {str(e)}"

def get_profile():
    try:
        response = sio.call('fetch_user_profile')
        return response
    except Exception as e:
        return f"Could not get fetch profile details: {str(e)}"

def logout():
    try:
        response = sio.call('signout')
        return response
    except Exception as e:
        return f"Logout failed: {str(e)}"