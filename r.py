#!/usr/bin/env python3

# Import the lib
import py_cui
import logging
from station import Station
from player import Player
from py_cui_extra import PyCUIExtra


class App:

    current_station = -1

    def __init__(self, master):
        # create station Manager
        self.sm = Station()
        # create player
        self.player = Player()
        # in the end the Tui
        self.master = master
        self.setup()

    def setup(self):

        self.master.status_bar.set_color(py_cui.BLACK_ON_GREEN)
        # grid station
        self.pnl_stations = self.master.add_scroll_menu('STATIONS', 0, 0,
                                                        row_span=10,
                                                        column_span=5)
        self.pnl_stations.set_color(py_cui.GREEN_ON_BLACK)
        self.pnl_stations.set_focus_text('Up/down to scroll, Enter to play,\
                                         Esc to exit.')

        # now playing grid
        self.pnl_info = self.master.add_scroll_menu('NOW', 10, 0, row_span=5,
                                                    column_span=5,
                                                    )
        self.pnl_info.set_color(py_cui.RED_ON_BLACK)
        self.master.move_focus(self.pnl_stations)

        # help grid
        self.pnl_help = \
            self.master.add_scroll_menu('HELP', 0, 5, row_span=15)
        self.pnl_help.set_color(py_cui.YELLOW_ON_BLACK)

        # handlers
        self.pnl_stations.add_key_command(py_cui.keys.KEY_ENTER, self.play)
        self.pnl_stations.add_key_command(py_cui.keys.KEY_M_LOWER,
                                          self.toggle_mute)

        # populate station grid
        for station in self.sm.stations:
            self.pnl_stations.add_item('{}'.format(station))

        self.update_info()

    def toggle_mute(self):
        self.player.toggle_mute()
        # TODO toggle view

    def play(self):
        # ll(help(self.pnl_stations))
        idx = self.pnl_stations.get_selected_item()
        self.current_station = self.sm.stations[idx]

        self.player.load_station(self.current_station)
        self.player.toggle()
        self.update_info(self.player.get_info())

    def update_info(self, info=-1):
        self.pnl_info.clear()

        if not self.player.is_playing:
            info = ['STOPPED', '', '']

        self.pnl_info.add_item('NOW:'.ljust(10, ' ') + info[0])
        self.pnl_info.add_item('GENERE:'.ljust(10, ' ') + info[1])
        self.pnl_info.add_item('RADIO:'.ljust(10, ' ') + info[2])


def ll(txt):
    logging.debug("---")
    logging.debug(txt)
    logging.debug("---")
    logging.debug("")


if __name__ == '__main__':
    logging.basicConfig(filename="app.log",
                        format='%(name)s [%(levelname)s] %(message)s',
                        datefmt='%H:%M:%S', level=logging.DEBUG)
    root = PyCUIExtra(15, 6)
    root.set_title('Mini-Radio-Player 3.0')
    ll(root.status_bar.__dict__)
    # root.set_title_color.set_color(py_cui.RED_ON_BLACK)
    root.toggle_unicode_borders()
    app = App(root)
    root.start()
