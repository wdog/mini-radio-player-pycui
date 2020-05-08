#!/usr/bin/env python3
"""
File: r.py
Author: wdog
Github: https://github.com/wdog
Description: Main Mini Radio Player
"""

# Import the lib
import py_cui
import logging
from station import Station
from player import Player
from py_cui_extra import PyCUIExtra
import threading
from datetime import datetime
import time


class App:

    # object radio selected
    current_station = -1

    def __init__(self, master):

        # create station Manager
        self.sm = Station()

        # create player
        self.player = Player()
        # in the end the Tui
        self.master = master
        self.setup()
        thread = threading.Thread(target=self.thread_function, args=())
        thread.daemon = True
        thread.start()

    def thread_function(self):
        while True:
            if self.player.is_playing:
                self.update_info(self.player.get_info())
            if self.master._stdscr:
                self.master._stdscr.timeout(10000)
            time.sleep(10)

    def setup(self):
        # setup color statu bar bottom
        self.master.status_bar.set_color(py_cui.BLACK_ON_GREEN)
        # -------------
        # grid station
        self.pnl_stations = \
            self.master.add_scroll_menu_extra('STATIONS', 0, 0,
                                              row_span=5,
                                              column_span=5)
        # setup color of station panel
        self.pnl_stations.set_color(py_cui.GREEN_ON_BLACK)
        # current row
        self.pnl_stations.set_item_selected_color(py_cui.BLACK_ON_GREEN)
        # radio active
        self.pnl_stations.set_item_active_color(py_cui.BLACK_ON_WHITE)

        # -------------
        # logo
        self.master.add_block_label(str(self.get_logo_text()), 1, 5, 4, 4)

        # -------------
        # help messages
        msg = []
        msg.append('⇅ select')
        msg.append('enter play/stop')
        msg.append('⇄ volume')
        msg.append('m mute')
        msg.append('q quit')
        msg = " " + " | ".join(msg)
        # help message on status bar
        self.pnl_stations.set_help_text(msg)
        # activate focus on station panel
        self.master.move_focus(self.pnl_stations)

        # -------------
        # now playing grid
        self.pnl_info = self.master.add_scroll_menu('NOW', 5, 0, row_span=3,
                                                    column_span=9)

        # setup color of info panel
        self.pnl_info.set_color(py_cui.RED_ON_BLACK)

        # slider
        self.slider = self.master.add_slider('volume', 8, 0, column_span=9,
                                             min_val=0, max_val=100, step=5)

        # -----------
        # handlers
        # -----------

        # play/pause
        self.pnl_stations.add_key_command(py_cui.keys.KEY_ENTER, self.play)
        # mute/unmute
        self.pnl_stations.add_key_command(py_cui.keys.KEY_M_LOWER,
                                          self.toggle_mute)
        # popup help
        self.pnl_stations.add_key_command(py_cui.keys.KEY_H_LOWER,
                                          self.help_menu)
        # update info
        self.pnl_stations.add_key_command(py_cui.keys.KEY_I_LOWER,
                                          self.update_station_info)
        # quit
        self.pnl_stations.add_key_command(py_cui.keys.KEY_Q_LOWER,
                                          self.exit_application)
        # volume up
        self.pnl_stations.add_key_command(py_cui.keys.KEY_RIGHT_ARROW,
                                          self.set_volume_up)
        # volume down
        self.pnl_stations.add_key_command(py_cui.keys.KEY_LEFT_ARROW,
                                          self.set_volume_down)
        # populate station grid
        for station in self.sm.stations:
            self.pnl_stations.add_item('{}: {}'.format(station.id,
                                       station.name))
        # ------------------
        # get stored setting
        # ------------------
        self.settings = self.sm.get_settings()

        logging.debug(self.settings)

        if 'volume' in self.settings:
            self.current_volume = int(self.settings['volume'])
        else:
            self.current_volume = 0
        # set stored volume
        self.set_volume(0)

    def toggle_mute(self):
        is_muted = self.player.toggle_mute()
        self.slider.disable(is_muted)

    def play(self):
        try:
            idx = self.pnl_stations.get_selected_item()
            self.current_station = self.sm.stations[idx]
            self.pnl_stations.set_selected(idx)
        except Exception:
            exit

        self.player.load_station(self.current_station)
        self.player.toggle()
        self.update_info(self.player.get_info())

    def update_station_info(self):
        self.update_info(self.player.get_info())

    def update_info(self, info=False):
        if not self.player.is_playing:
            info = ['STOPPED', '', '']
        self.pnl_info.clear()
        self.pnl_info.add_item('NOW:'.ljust(8, ' ') + info[0])
        self.pnl_info.add_item('GENERE:'.ljust(8, ' ') + info[1])
        self.pnl_info.add_item('RADIO:'.ljust(8, ' ') + info[2])
        self.pnl_info.add_item("TIME:   {}".format(
                               datetime.now().strftime('%X')))

    def exit_application(self):
        exit()

    def set_volume_up(self):
        # workaround cannot pass args to callback
        self.set_volume(1)

    def set_volume_down(self):
        # workaround cannot pass args to callback
        self.set_volume(-1)

    def set_volume(self, direction):
        # slider
        self.current_volume = \
            self.slider.set_slider_value(self.current_volume, direction)
        # player
        self.player.set_volume(self.current_volume)
        # store value into db
        self.sm.store_setting('volume', self.current_volume)

    def get_logo_text(self):
        out = ""
        out += "█▀▄▀█ █ █▄ █ █\n "
        out += "█ ▀ █ █ █ ▀█ █\n "
        out += "\n"
        out += "█▀█ ▄▀█ █▀▄ █ █▀█\n"
        out += "█▀▄ █▀█ █▄▀ █ █▄█\n"
        out += "\n"
        out += "█▀█ █   ▄▀█ █▄█ █▀▀ █▀█\n"
        out += "█▀▀ █▄▄ █▀█  █  ██▄ █▀▄\n"
        return out

    def help_menu(self):
        msg_help = "m) mute\n"
        msg_help += "^ Select Station\n"
        msg_help += "<> Volume up/down\n"
        msg_help += "q) quit\n"
        msg_help += "<esc> to exit menu\n"
        msg_help += "\n"

        self.master.show_message_popup('HELP', msg_help)

    def action_menu(self, element):
        logging.info(element)
        pass


if __name__ == '__main__':
    logging.basicConfig(filename="app.log", format='%(asctime)s - %(name)s - '
                        '%(levelname)s: %(message)s', datefmt='%H:%M:%S',
                        level=logging.DEBUG)
    logging.info("\n----\n")
    # 9 rows x 3 cols
    root = PyCUIExtra(9, 9)
    root.set_title('Mini-Radio-Player 3.0')
    root.toggle_unicode_borders()
    app = App(root)
    root.start()
