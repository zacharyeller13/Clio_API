import os
from get_authorization import Clio
from Clio_API_GetAuthorization import get_config, get_client_id, get_client_secret

def main():

    curpath = os.path.dirname(os.path.realpath(__file__))
    config_file = os.path.join(curpath, "config.ini")
    config_parser = get_config(config_file)
    client_id = get_client_id(config_parser)
    client_secret = get_client_secret(config_parser)

    session = Clio(client_id=client_id)
    print(session.authorization_url(session.auth_url)[0])
    authorization_response = input("Enter the full callback URL: ")
    session.fetch_token(
        session.token_url,
        authorization_response=authorization_response,
        client_secret=client_secret,
        include_client_id=True
    )

    print(session.authorized)
    print(session.deauthorize())

if __name__ == "__main__":

    main()