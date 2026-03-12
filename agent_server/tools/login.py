from .base import post
from utils.email import is_valid_email

def validate_credentials(payload):
    email = (payload.get('email'))
    password = (payload.get('password'))

    if ( is_valid_email(email) != True):
        return f"{email} is not a valid email please try again"
        
    if ( len(password) < 6):
        return "Password must be at least 6 characters"
    
    return True
    
def login(payload):
    return post("/login", payload)