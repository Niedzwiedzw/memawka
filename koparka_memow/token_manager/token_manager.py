from memawka import settings
from koparka_memow.settings import SETTINGS as FB_SETTINGS
import requests
import os


class TokenManager:

    @classmethod
    def _read_token(cls):
        with open(os.path.join(os.path.join(settings.BASE_DIR, 'koparka_memow'),
                               'access_token.txt'), 'r') as f:
            return f.read()

    @classmethod
    def _save_token(cls, token):
        with open(os.path.join(os.path.join(settings.BASE_DIR, 'koparka_memow'),
                               'access_token.txt'), 'w') as f:
            f.write(token)

    @classmethod
    def get_token(cls):
        try:
            return cls._read_token()

        except FileNotFoundError as e:

            cls._save_token(token='')
            print("insert a token into",
                  os.path.join(os.path.join(settings.BASE_DIR, 'koparka_memow'), 'access_token.txt')
                  )
            return None

    @classmethod
    def refresh_token(cls, token=None):
        if token is None:
            token = cls.get_token()
        link = (
            f'https://graph.facebook.com/oauth/access_token?'
            f'grant_type=fb_exchange_token&'
            f'client_id={FB_SETTINGS["app-id"]}&'
            f'client_secret={FB_SETTINGS["app-secret"]}&'
            f'fb_exchange_token={token}'
        )

        response = requests.get(link)
        cls._save_token(response.json()['access_token'])


if __name__ == '__main__':
    TokenManager.refresh_token()
