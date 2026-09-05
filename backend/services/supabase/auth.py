from . import supabase


def sign_up_user(email, password):
    response = supabase.auth.sign_up({
        "email": email,
        "password": password,
    })
    print("Supabase response received:", response)
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