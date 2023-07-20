import requests

# Refresh timer (milliseconds, >5000)
refresh_timer = 10000


# API base url
class BaseUrl:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(BaseUrl, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "base_url"):
            self.base_url = 'http://127.0.0.1:8000/api/'

    def set_base_url(self):
        try:
            print(requests.get('http://127.0.0.1:8000/').status_code)
        except Exception:
            self.base_url = 'https://sheltered-oasis-16253-bb111470476b.herokuapp.com/api/'

    def get_base_url(self):
        return self.base_url


# Security level
level = 'is_staff'

# Define the colors
primary_color = "#D27F35"
secondary_color = "#3A3238"
surface_color = "#1e1e1e"
dark_color = "#161315"
light_color = "#b8b8b8"
# Legend colors
finished = "green"
started = "yellow"
soon = "red"
tocome = light_color

# Bookings font
fsize = "20px"
