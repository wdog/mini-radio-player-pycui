import json
from radio_station import RadioStation


class Station:
    """STATION CLASS - MANAGES RADIO LIST"""
    stations = []

    def __init__(self):
        self.load_stations_list()

    def load_stations_list(self):
        """Load radio station list"""
        with open('radio.json') as f:
            sts = json.load(f)

        self.stations = []
        for s in sts:
            self.stations.append(RadioStation(s))

    def change_order(self, o_src=-1, o_dst=-1):

        if (not o_src or not o_dst):
            return

        src = o_src[0]
        dst = o_dst[0]

        lines = []
        with open('radio.json') as f:
            lines = json.load(f)

        # SWAP LINES
        # lines[src], lines[dst] = lines[dst], lines[src]

        moved = lines.pop(src)
        lines.insert(dst, moved)

        with open('radio.json', 'w') as f:
            json.dump(lines, f, indent=4)

    def __iter__(self):
        return self

    def __next__(self):
        return self
