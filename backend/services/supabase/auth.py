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
            .insert({'id':response.user.id,'username':username,'full_name':full_name,'avatar_url':avatar_url})
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