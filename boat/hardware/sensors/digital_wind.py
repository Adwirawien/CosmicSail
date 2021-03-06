import arrow
import requests
from utility.coordinates import get_distance


class DigitalWindSensor:
    name = ""
    prev_state = {}

    wind_data = {}

    debug = False
    debug_wind_dir = 180
    debug_wind_speed = 5

    def __init__(self, name, token):
        self.name = name
        self.token = token

    def get_value(self):
        return {
            "time": self.get_time(),
            "gust": self.get_gust(),
            "direction": self.get_wind_direction(),
            "speed": self.get_wind_speed()
        }

    def get_name(self):
        return self.name

    def get_time(self):
        if 'dt' not in self.wind_data:
            return None
        return arrow.get(self.wind_data['dt']).to('local').timestamp

    # wind direction in degrees
    def get_wind_direction(self):
        if self.debug:
            return self.debug_wind_dir

        if 'deg' not in self.wind_data:
            return 0
        return self.wind_data['deg']

    # wind speed in m/s
    def get_wind_speed(self):
        if self.debug:
            return self.debug_wind_speed

        if 'speed' not in self.wind_data:
            return 0
        return self.wind_data['speed']

    # wind gusts in m/s
    def get_gust(self):
        if 'gust' not in self.wind_data:
            return None
        return self.wind_data['gust']

    def fetch_wind(self, lat, lng):
        if 'lat' in self.wind_data and get_distance(self.wind_data['lat'], self.wind_data['lng'], lat, lng) < 25:
            return None

        response = requests.get(
            'http://api.openweathermap.org/data/2.5/weather',
            params={
                'lat': lat,
                'lon': lng,
                'appid': self.token
            }
        )

        self.wind_data = response.json()['wind']
        self.wind_data['lat'] = lat
        self.wind_data['lng'] = lng
        return None

    def has_changed(self):
        """compares changes in the wind data for telemetry purposes"""
        changed = self.get_meta() != self.prev_state
        self.prev_state = self.get_meta()

        return changed

    def get_meta(self):
        return self.get_value()
