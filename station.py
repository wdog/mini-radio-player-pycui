from radio_station import RadioStation
from radiodb import RadioDB


class Station:
    """STATION CLASS - MANAGES RADIO LIST"""
    stations = []

    def __init__(self):
        self.radio_db = RadioDB('radio.db')
        self.load_stations_list()

    def load_stations_list(self):
        self.stations = []
        for row in self.radio_db.read_table_radio():
            self.stations.append(RadioStation(row))

    def get_stations(self):
        stations = []
        for row in self.radio_db.read_table_radio():
            stations.append(RadioStation(row))
        return stations

    def get_settings(self):
        settings = {}
        for row in self.radio_db.get_settings():
            settings[row['param']] = row['value']
        return settings

    def store_setting(self, key, value):
        self.radio_db.store_setting(key, value)

    def add_view(self, station_id):
        self.radio_db.add_view(station_id)
