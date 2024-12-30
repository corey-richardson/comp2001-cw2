import requests

# https://dle.plymouth.ac.uk/pluginfile.php/3528870/mod_resource/content/1/Test%20Authenticator%20in%20Python.pdf

AUTH_URL = "https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users"

def authenticate(email, password):
    # Create request body JSON
    credentials = {
        "email" : email,
        "password" : password
    }
    
    response = requests.post(AUTH_URL, json=credentials)
    
    if response.status_code == 200:
        try:
            json_response = response.json()
            
            if json_response[1] == "True": # User credentials exists and match
                return True
            
        except requests.JSONDecodeError:
            pass # Handled during return
        
    print("Authentication failed.")
    print(f"Status Code: {response.status_code}.")
    print(f"Content: {response.text}.\n")
    return False
    
# Only runs if the script is ran directly for testing, not if `authenticate` is called from elsewhere.
if __name__ == "__main__":
    exp_pass_result = authenticate("tim@plymouth.ac.uk", "COMP2001!")
    exp_fail_resilt = authenticate("corey@gmail.com", "Password1!")
    
    # If an AssertionError is raised, there's a problem with the authenticator!
    # "Authentication failed." print statement does not indicate a problem, this is expected behaviour.
    assert exp_pass_result == True
    assert exp_fail_resilt == False
    