import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from backend.config import sio
from backend.services.supabase.auth import login_user, sign_up_user
def register_auth_sockets():

    @sio.on('login')
    def login(data):
        try:
            login_user(data['email'],data['password'])
            return {'success':True}

        except Exception as e:
            return {'success': False, 'error': str(e)}

    @sio.on('signup')
    def signup(data):
        print("Backend received data:", data)
        try:
            sign_up_user(data['email'],data['password'])
            return {'success':True}
        except Exception as e:
            return {'success': False, 'error': str(e)}
        