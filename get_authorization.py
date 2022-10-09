from requests_oauthlib import OAuth2Session
from configparser import ConfigParser

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
        **kwargs
    ):
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
            **kwargs
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