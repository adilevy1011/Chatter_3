
from socket_client import sio

def login(email,password):
    try:
        response = sio.call('login',{'email': email, 'password': password},timeout=15)
        print("Server response:", response)
        return response
    except Exception as e:
        return f"Login failed: {str(e)}"

def login_with_token(token):
    try:
        response = sio.call('login_with_token', {'token': token}, timeout=15)
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