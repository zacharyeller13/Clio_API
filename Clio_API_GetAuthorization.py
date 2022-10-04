from requests_oauthlib import OAuth2Session

# Define parameters
client_id = r""
client_secret = r""


def Clio(
    client_id: str, 
    client_secret: str, 
    redirect_uri: str="https://app.clio.com/oauth/approval", 
    auth_url: str="https://app.clio.com/oauth/authorize",
    token_url: str="https://app.clio.com/oauth/token"
) -> OAuth2Session:
    """
    Generate an OAuth Session Object to be used for authenticated requests

    Arguments:
        - client_id
        - client_secret
        - auth_url: Clio's Authorization URL
        - token_url: Clio's Token URL
        - redirect_uri: if none for your app; Clio allows https://app.clio.com/oauth/approval
    """
    # Create a client
    oauth = OAuth2Session(
        client_id, 
        redirect_uri=redirect_uri,
    )

    # Obtain authorization url to be visited by User
    authorization_url, _ = oauth.authorization_url(
        auth_url
    )

    # Print auth url and request input of authorization code
    print(f"Please go to {authorization_url} and authorize access")
    authorization_response = input("Enter the full callback URL")

    # Define access token from using authorization response code
    token = oauth.fetch_token(
        token_url,
        authorization_response=authorization_response,
        client_secret=client_secret,
        include_client_id=True
    )

    return oauth