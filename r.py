#!/usr/bin/env python3

# Import the lib
import py_cui
import logging
from station import Station
from player import Player


class App:

    current_station = -1

    def __init__(self, master):
        self.master = master
        self.sm = Station()
        self.player = Player()
        self.setup()

    def setup(self):

        # grid station
        self.pnl_stations = self.master.add_scroll_menu('STATIONS', 0, 0,
                                                        row_span=10,
                                                        column_span=5)

        self.pnl_stations.set_color(py_cui.GREEN_ON_BLACK)

        # now playing grid
        self.pnl_info = self.master.add_scroll_menu('NOW', 10, 0, row_span=5,
                                                    column_span=5)
        self.pnl_info.set_color(py_cui.RED_ON_BLACK)

        # help grid
        self.pnl_help = \
            self.master.add_scroll_menu('HELP', 0, 5, row_span=15)
        self.pnl_help.set_color(py_cui.YELLOW_ON_BLACK)
        self.pnl_help.set_color_rules(py_cui.CYAN_ON_BLACK)

        # handlers
        self.pnl_stations.add_key_command(py_cui.keys.KEY_ENTER, self.play)

        # populate station grid
        for station in self.sm.stations:
            self.pnl_stations.add_item('{}'.format(station))
        self.master.move_focus(self.pnl_stations)

    def play(self):
        # ll(help(self.pnl_stations))
        idx = self.pnl_stations.get_selected_item()
        self.current_station = self.sm.stations[idx]

        self.player.load_station(self.current_station)
        self.player.toggle()


def ll(txt):
    logging.debug("---")
    logging.debug(txt)
    logging.debug("---")
    logging.debug("")


if __name__ == '__main__':
    logging.basicConfig(filename="app.log",
                        format='%(name)s [%(levelname)s] %(message)s',
                        datefmt='%H:%M:%S', level=logging.DEBUG)
    root = py_cui.PyCUI(15, 6)
    root.set_title('Mini-Radio-Player 3.0')
    root.toggle_unicode_borders()
    app = App(root)
    root.start()
