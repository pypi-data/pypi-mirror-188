import time

import jwt
import requests


def is_token_expired(token):
    try:
        decoded = jwt.decode(token, options={"verify_signature": False})
        if 'exp' in decoded:
            exp_time = decoded['exp']
            current_time = time.time()
            # time in seconds
            return current_time - 30 > exp_time
        return False
    except jwt.DecodeError:
        raise
    except jwt.ExpiredSignatureError:
        return True


class TokenHolder:
    def __init__(self, **kwargs):
        self.domain = kwargs['domain']
        self.realm = kwargs['realm']
        self.client_id = kwargs['client_id']
        self.access_token = kwargs.get('access_token', '')
        self.refresh_token = kwargs.get('refresh_token', '')

    def get_tokens_with_credentials(self, username, password):
        data = {
            "grant_type": "password",
            "client_id": self.client_id,
            "username": username,
            "password": password
        }
        response = requests.post(f'https://{self.domain}/auth/realms/{self.realm}/protocol/openid-connect/token', data=data)
        response.raise_for_status()
        self.access_token = response.json()["access_token"]
        self.refresh_token = response.json()["refresh_token"]

    def _refresh_tokens(self):
        payload = f'grant_type=refresh_token&refresh_token={self.refresh_token}&client_id={self.client_id}'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.post(f'https://{self.domain}/auth/realms/{self.realm}/protocol/openid-connect/token', headers=headers, data=payload)
        response.raise_for_status()
        # TODO error handling!!
        self.access_token = response.json()["access_token"]
        self.refresh_token = response.json()["refresh_token"]

    def get_token(self):
        if is_token_expired(self.access_token):
            self._refresh_tokens()
        return self.access_token
