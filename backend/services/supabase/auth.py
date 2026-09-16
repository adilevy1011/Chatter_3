from . import supabase


def sign_up_user(email, password,username=None,full_name=None,avatar_url=None):
    response = supabase.auth.sign_up({
        "email": email,
        "password": password,
        "options": {
            "data": {
                "display_name": username,
                "full_name": full_name
            }
        }
    })
    if response.user is not None:
        profiles_response = (
            supabase.table("profiles")
            .insert({'id':response.user.id,'username':username,'full_name':full_name,'avatar_url':avatar_url,'email':email})
            .execute()
        )
    return response

def login_user(email, password):
    try:
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        return response
    except Exception as e:
        raise Exception(f'Login failed: {str(e)}')

def login_with_token_user(access_token, refresh_token):
    try:
        response = supabase.auth.set_session(access_token, refresh_token)
        if not response.user or not response.session:
            raise Exception("Invalid or expired session token")

        verified_user = supabase.auth.get_user(response.session.access_token)
        if not verified_user or not verified_user.user:
            raise Exception("Session could not be verified")

        return response
    except Exception as e:
        raise Exception(f'Token login failed: {str(e)}')

def logout_user():
    response = supabase.auth.sign_out()
    return response

def get_user_profile():
    session = supabase.auth.get_session()
    if session:
        response = (
            supabase.table('profiles')
            .select('*')
            .eq('id',session.user.id)
            .single()
            .execute()
        )
        return response.data
    else:
        raise Exception(f'Could not verify session')
