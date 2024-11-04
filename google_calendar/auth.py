from google_auth_oauthlib.flow import InstalledAppFlow

def authenticate_google_account():
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    
    # Initialize the flow using the client_secret.json file
    flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
    creds = flow.run_local_server(port=0)
    
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())
    
    return creds
