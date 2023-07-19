import requests

import config


class TokenGetter:
    def __init__(self):
        self.url = 'http://127.0.0.1:8000/api/token/'

    def get_token(self, username, password):
        data = {
            'username': username,
            'password': password
        }
        response = requests.post(self.url, data=data)

        if response.status_code == 200:
            json_data = response.json()
            token = json_data['token']
            return token
        else:
            return response.status_code


class TokenAuth:
    def __init__(self, token=None):
        self.level = config.level
        self.url = 'http://127.0.0.1:8000/api/' + self.level + '/'
        self._token = token

    def authorization(self):
        if self._token is not None:
            headers = {'Authorization': f'Token {self._token}'}
            try:
                response = requests.get(self.url, headers=headers)
                response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
                body = response.json()
            except requests.exceptions.RequestException as e:
                print(f'Request failed: {e}')
                return False
            return bool(body[str(self.level)])

    def get_token(self):
        if self._token is None:
            print('Access token not found')
        else:
            return self._token


def main():
    username = input('Enter your username: ')
    password = input('Enter your password: ')

    token_getter = TokenGetter()
    token_auth = TokenAuth(token_getter.get_token(username, password))
    token_auth.authorization()


if __name__ == '__main__':
    main()
