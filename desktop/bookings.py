from datetime import datetime, timedelta

import requests

import auth
import config


class APIBookingsClient:
    def __init__(self, token=None, date=None):
        self.base_url = config.BaseUrl().get_base_url()
        self.url = self.base_url + 'booking/'
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


class APIScenariosClient:
    def __init__(self):
        self.base_url = config.BaseUrl().get_base_url()
        self.scenarios = self.get_scenarios()

    def get_scenarios(self):
        url = self.base_url + 'scenario/'
        try:
            response = requests.get(url)
            response.raise_for_status()
            response = response.json()
            return response["results"]
        except Exception as e:
            print(f'Request failed: {e}')


class APIUserClient:

    def __init__(self, token):
        self.base_url = config.BaseUrl().get_base_url()
        self.user = self.get_user_from_id(token)

    def get_user_from_id(self, token):
        url = self.base_url + 'user/' + str(self.user) + '/'
        headers = {'Authorization': f'Token {token}'}
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            response = response.json()
            return response['username'], response['first_name'], response['last_name'], response['email']
        except Exception as e:
            print(f'Request failed: {e}')


class BookingElement:

    def __init__(self, booking, scenarios_json):
        self.base_url = config.BaseUrl().get_base_url()
        self.id = booking['id']
        self.user = booking['user']
        self.scenario = booking['scenario']
        self.room = booking['room']
        self.time = booking['time']
        self.num_players = booking['num_players']
        self.start_dt = self.to_datetime(booking['start_time'])
        self.start_time = self.split_time(self.start_dt)
        self.gameover_dt = self.to_datetime(booking['gameover_time'])
        self.gameover_time = self.split_time(self.gameover_dt)
        self.chrono = booking['chrono']
        (self.scn_name, self.duration) = self.get_scenario_details(scenarios_json)

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

    def get_scenario_details(self, scenarios_json):
        for scenario in scenarios_json:
            if scenario["id"] == self.scenario:
                (h, m, s) = scenario['duration'].split(':')
                return scenario['name'], timedelta(hours=int(h), minutes=int(m), seconds=int(s))


def main():
    username = input('Enter your username: ')
    password = input('Enter your password: ')

    token_getter = auth.TokenGetter()
    token_auth = auth.TokenAuth(token_getter.get_token(username, password))
    bookings = APIBookingsClient(token_auth.get_token())
    print(bookings.get_data())


if __name__ == '__main__':
    main()
