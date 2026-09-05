import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from backend.config import sio
from backend.services.supabase.auth import login_user, sign_up_user, login_with_token_user


def auth_result(response):
    session = getattr(response, "session", None)
    return {
        "success": True,
        "token": session.access_token if session is not None else None,
        "user": response.user.id if response.user is not None else None,
    }


def register_auth_sockets():

    @sio.on('login')
    def login(data):
        try:
            return auth_result(login_user(data['email'], data['password']))

        except Exception as e:
            return {'success': False, 'error': str(e)}

    @sio.on('signup')
    def signup(data):
        print("Backend received data:", data)
        try:
            return auth_result(
                sign_up_user(
                    data['email'],
                    data['password'],
                    data['username'],
                    data['full_name'],
                    data['avatar_url'],
                )
            )
        except Exception as e:
            return {'success': False, 'error': str(e)}

    @sio.on('login_with_token')
    def login_with_token(data):
        try:
            token = data.get('token')
            if not token:
                return {'success': False, 'error': 'Token is missing'}

            res = login_with_token_user(token)
            return {
                'success': True,
                'user': res.user.id if res.user else None
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
        