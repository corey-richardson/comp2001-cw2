import requests
from datetime import datetime, timedelta, timezone
import jwt
from flask import request, abort
from functools import wraps

# https://dle.plymouth.ac.uk/pluginfile.php/3528870/mod_resource/content/1/Test%20Authenticator%20in%20Python.pdf

AUTH_URL = "https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users"
USER_URL = "http://localhost:8000/api/user"

def authenticate():
    body = request.get_json()
    
    if not body or not body.get("email") or not body.get("password"):
        abort(400, "Email and password fields are required.")
        
    # Create request body JSON
    credentials = {
        "email" : body["email"],
        "password" : body["password"]
    }
    
    try:
        response = requests.post(AUTH_URL, json=credentials)
    except requests.exceptions.RequestException as e:
        abort(500, f"Failed to authenticate: {str(e)}")
    
    if response.status_code == 200:
        try:
            json_response = response.json()
            
            if json_response[1] == "True": # User credentials exists and match
                # API Database
                user_data = {
                    "email" : body["email"],
                    "role"  : "ADMIN"
                }
                
                try:
                    response = requests.post(USER_URL, json=user_data)
                except Exception as e:
                    print("Failed to add new user: ", str(e))
                
                # JWT
                expiration = datetime.now(timezone.utc) + timedelta(hours=1)
                payload = {
                    "email" : body["email"],
                    "exp"   : expiration
                }
                
                token = jwt.encode(payload, "SECRET_KEY_DONT_LOOK_AT_ME", algorithm = "HS256")
                return {"token" : token}, 200
            
        except requests.JSONDecodeError:
            abort(500, f"Error processing authentication response: {str(e)}")
        
    abort(401, "Invalid credentials")
    