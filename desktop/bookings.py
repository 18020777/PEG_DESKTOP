import requests
from datetime import datetime, timedelta

import auth


class APIBookingsClient:
    def __init__(self, token=None, date=None):
        self.url = 'http://127.0.0.1:8000/api/booking/'
        self._token = token
        if date is not None:
            self.url = self.url + '?date=' + str(date)

    def get_data(self):

        if self._token is None:
            print('Access token not found')
            return None

        headers = {'Authorization': f'Token {self._token}'}

        try:
            response = requests.get(self.url, headers=headers)
            response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f'Request failed: {e}')
            return None


class BookingElement:

    def __init__(self, booking, token):
        self.id = booking['id']
        self.user = booking['user']
        (self.username, self.first_name, self.last_name, self.email) = self.get_user_from_id(token)
        self.scenario = booking['scenario']
        (self.scn_name, self.duration) = self.get_scenario_details()
        self.time = booking['time']
        self.num_players = booking['num_players']
        self.start_dt = self.to_datetime(booking['start_time'])
        self.start_time = self.split_time(self.start_dt)
        self.gameover_dt = self.to_datetime(booking['gameover_time'])
        self.gameover_time = self.split_time(self.gameover_dt)
        self.chrono = booking['chrono']

    @staticmethod
    def split_time(time_to_split):
        if time_to_split is not None:
            return time_to_split.time()
        else:
            return None

    @staticmethod
    def to_datetime(dt_to_format):
        if dt_to_format is not None:
            return datetime.strptime(str(dt_to_format).split('.')[0], '%Y-%m-%dT%H:%M:%S')
        else:
            return None

    def get_user_from_id(self, token):
        url = 'http://127.0.0.1:8000/api/user/' + str(self.user) + '/'
        headers = {'Authorization': f'Token {token}'}
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            response = response.json()
            return response['username'], response['first_name'], response['last_name'], response['email']
        except Exception as e:
            print(f'Request failed: {e}')

    def get_scenario_details(self):
        url = 'http://127.0.0.1:8000/api/scenario/' + str(self.scenario) + '/'
        try:
            response = requests.get(url)
            response.raise_for_status()
            response = response.json()
            (h, m, s) = response['duration'].split(':')
            return response['name'], timedelta(hours=int(h), minutes=int(m), seconds=int(s))
        except Exception as e:
            print(f'Request failed: {e}')


def main():
    username = input('Enter your username: ')
    password = input('Enter your password: ')

    token_getter = auth.TokenGetter()
    token_auth = auth.TokenAuth(token_getter.get_token(username, password))
    bookings = APIBookingsClient(token_auth.get_token())
    print(bookings.get_data())


if __name__ == '__main__':
    main()
