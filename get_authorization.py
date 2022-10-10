from requests_oauthlib import OAuth2Session
from configparser import ConfigParser

class Config(ConfigParser):
    """
    ConfigParser subclass for reading config containing Clio client_id and client_secret
    """

    def __init__(self, config_file) -> None:
        super().__init__()
        self.client_id = config_file
        self.client_secret = config_file

    @property
    def client_id(self) -> str:
        return self.__client_id

    @client_id.setter
    def client_id(self, config_file) -> None:
        self.read(config_file)
        self.__client_id = self.get("ClientInfo", "client_id")

    @property
    def client_secret(self) -> str:
        return self.__client_secret

    @client_secret.setter
    def client_secret(self, config_file) -> None:
        self.read(config_file)
        self.__client_secret = self.get("ClientInfo", "client_secret")

class Clio(OAuth2Session):
    
    def __init__(
        self, 
        client_id=None,
        client=None,
        auto_refresh_url=None,
        auto_refresh_kwargs=None,
        scope=None,
        redirect_uri="https://app.clio.com/oauth/approval",
        token=None,
        state=None,
        token_updater=None,
        auth_url="https://app.clio.com/oauth/authorize",
        token_url="https://app.clio.com/oauth/token",
    ) -> None:
        super().__init__(
            client_id,
            client,
            auto_refresh_url,
            auto_refresh_kwargs,
            scope,
            redirect_uri,
            token,
            state,
            token_updater,
        )
        self.auth_url = auth_url
        self.token_url = token_url

    def deauthorize(self) -> str:
        resp = self.post("https://app.clio.com/oauth/deauthorize", params={
            "token": self.token
        })

        if resp.ok:
            return "Successfully deauthorized"
        else:
            return "Something went wrong"