
from socket_client import sio

def login(email,password):
    try:
        response = sio.call('login',{'email': email, 'password': password},timeout=15)
        print("Server response:", response)
        return response
    except Exception as e:
        return f"Login failed: {str(e)}"
def signup(email,password):
    try:
        response = sio.call('signup',{'email': email, 'password': password},timeout=15)
        print("Server response:", response)
        return response
    except Exception as e:
        return f"signup failed: {str(e)}"