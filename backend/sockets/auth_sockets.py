import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from backend.config import sio
from backend.services.supabase.auth import login_user, sign_up_user, login_with_token_user, logout_user,get_user_profile


def auth_result(response):
    session = getattr(response, "session", None)
    return {
        "success": True,
        "access_token": session.access_token if session is not None else None,
        "refresh_token": session.refresh_token if session is not None else None,
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
            access_token = data.get('access_token')
            refresh_token = data.get('refresh_token')
            if not access_token or not refresh_token:
                return {'success': False, 'error': 'Session tokens are missing'}

            return auth_result(
                login_with_token_user(access_token, refresh_token)
            )
        except Exception as e:
            return {'success': False, 'error': str(e)}

    @sio.on('signout')
    def signout_user():
        logout_user()

    @sio.on('fetch_user_profile')
    def get_profile():
        try:
            response = get_user_profile()
            return response
        except Exception as e:
            return {'success': False, 'error': str(e)}