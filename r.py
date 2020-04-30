#!/usr/bin/env python3

"""
Main Radio
Author: wdog
"""

# Import the lib
import py_cui
import logging
from station import Station
from player import Player
from py_cui_extra import PyCUIExtra


class App:

    current_station = -1
    current_volume = 0

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
        self.pnl_stations = \
            self.master.add_scroll_menu_extra('STATIONS', 0, 0,
                                              row_span=5,
                                              column_span=3)

        self.pnl_stations.set_color(py_cui.GREEN_ON_BLACK)
        self.pnl_stations.set_item_selected_color(py_cui.BLACK_ON_GREEN)
        self.pnl_stations.set_item_active_color(py_cui.BLACK_ON_WHITE)
        msg = []
        msg.append(' enter - play/stop')
        msg.append(' < > volume')
        msg.append(' m - mute')
        msg.append(' i - update info')
        msg.append(' q quit')

        msg = " | ".join(msg)
        self.pnl_stations.set_focus_text(msg)
        self.master.move_focus(self.pnl_stations)

        # now playing grid
        self.pnl_info = self.master.add_scroll_menu('NOW', 5, 0, row_span=3,
                                                    column_span=3)
        self.pnl_info.set_color(py_cui.RED_ON_BLACK)

        # slider
        self.slider = self.master.add_slider('volume', 8, 0, column_span=3,
                                             min_val=0, max_val=100, step=5)
        # handlers
        self.pnl_stations.add_key_command(py_cui.keys.KEY_ENTER, self.play)
        self.pnl_stations.add_key_command(py_cui.keys.KEY_M_LOWER,
                                          self.toggle_mute)
        self.pnl_stations.add_key_command(py_cui.keys.KEY_Q_LOWER,
                                          self.exit_application)

        self.pnl_stations.add_key_command(py_cui.keys.KEY_RIGHT_ARROW,
                                          self.set_volume_up)
        self.pnl_stations.add_key_command(py_cui.keys.KEY_LEFT_ARROW,
                                          self.set_volume_down)
        # populate station grid
        for station in self.sm.stations:
            self.pnl_stations.add_item('{}'.format(station))

        self.update_info()

    def toggle_mute(self):
        is_muted = self.player.toggle_mute()
        self.slider.disable(is_muted)

    def play(self):
        idx = self.pnl_stations.get_selected_item()
        self.current_station = self.sm.stations[idx]

        self.player.load_station(self.current_station)
        self.player.toggle()
        self.update_info(self.player.get_info())

        self.current_volume = self.player.get_volume()
        # get old volume
        self.set_volume(0)

    def update_info(self, info=False):
        self.pnl_info.clear()

        if not self.player.is_playing:
            info = ['STOPPED', '', '']

        self.pnl_info.add_item('NOW:'.ljust(10, ' ') + info[0])
        self.pnl_info.add_item('GENERE:'.ljust(10, ' ') + info[1])
        self.pnl_info.add_item('RADIO:'.ljust(10, ' ') + info[2])

    def exit_application(self):
        exit()

    def set_volume_up(self):
        self.set_volume(1)

    def set_volume_down(self):
        self.set_volume(-1)

    def set_volume(self, direction):
        # slider
        self.current_volume = \
            self.slider.set_slider_value(self.current_volume, direction)
        # player
        self.player.set_volume(self.current_volume)
        logging.info(self.current_volume)


def ll(txt):
    logging.debug("---")
    logging.debug(txt)
    logging.debug("---")
    logging.debug("")


if __name__ == '__main__':
    logging.basicConfig(filename="app.log",
                        format='%(name)s [%(levelname)s] %(message)s',
                        datefmt='%H:%M:%S', level=logging.DEBUG)
    logging.info("\n\n\n\n\n\n\n\n\n\n")
    # 9 rows x 3 cols
    root = PyCUIExtra(9, 3)
    root.set_title('Mini-Radio-Player 3.0')
    root.toggle_unicode_borders()
    app = App(root)
    root.start()
