from datetime import datetime, timedelta, timezone
from functools import wraps

import jwt
import requests
from flask import abort, request

# https://dle.plymouth.ac.uk/pluginfile.php/3528870/mod_resource/content/1/Test%20Authenticator%20in%20Python.pdf

# URLs for Authentication API, and user management endpoint
AUTH_URL = "https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users"
USER_URL = "http://localhost:8000/api/user"

SECRET_KEY = "SECRET_KEY_DONT_LOOK_AT_ME"

def authenticate():
    """
    Handles user authentication by validating an email and password with 
    the University of Plymouth Authenticator API.
    """
    # Retrieve request body and check validity
    body = request.get_json()
    if not body or not body.get("email") or not body.get("password"):
        abort(400, "Email and password fields are required.")
        
    # Create request body JSON
    credentials = {
        "email" : body["email"],
        "password" : body["password"]
    }
    
    try:
        # POST request to Authenticator API
        response = requests.post(AUTH_URL, json=credentials)
    except requests.exceptions.RequestException as e:
        abort(500, f"Failed to authenticate: {str(e)}")
    
    # Was authentication successful?
    if response.status_code == 200:
        try:
            json_response = response.json()
            
            if json_response[1] == "True":             
                # Generate a JWT Token
                expiration = datetime.now(timezone.utc) + timedelta(hours=1)
                payload = {
                    "email" : body["email"],
                    "exp"   : expiration
                }
                
                token = jwt.encode(payload, SECRET_KEY, algorithm = "HS256")
            else:
                abort(401, "Invalid credentials")
            
        except requests.JSONDecodeError:
            abort(500, f"Error processing authentication response: {str(e)}")
            
        # Add user to the server database with an ADMIN role
        user_data = {
            "email" : body["email"],
            "role"  : "ADMIN"
        }
        
        auth_header = {
            "Authorization" : "Bearer " + token
        }
        
        try:
            response = requests.post(USER_URL, json=user_data, headers=auth_header)
        except Exception as e:
            print("Failed to add new user: ", str(e))
            
        return {"token" : token}, 200
            
    else:  
        abort(401, "Invalid credentials")
    

def validate_token():
    """
    Decodes and validates a JWT taken token from the 
    "Authorization" header of the request.
    """
    auth_header = request.headers.get("Authorization")
        
    if not auth_header:
        abort(401, "Missing token.")
    if not auth_header.startswith("Bearer "):
        abort(401, "Invalid token format.")

    # Parse the token
    token = auth_header.split(" ")[1].strip()

    try:
        # Decode
        jwt.decode(token, SECRET_KEY, algorithms = ["HS256"])
    except jwt.ExpiredSignatureError:
        abort(401, "Token expired")
    except jwt.InvalidTokenError:
        abort(401, "Invalid token")


def require_auth(f):
    """
    Decorator to mark endpoint methods that should be protected.
    """
    # print(f.__name__)
    @wraps(f)
    def decorator(*args, **kwargs):
        validate_token()
        return f(*args, **kwargs)
    return decorator    
