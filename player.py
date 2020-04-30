import vlc
import time
import logging


class Player:

    current_station = None
    is_playing = False
    instance = None
    volume = 30

    def __init__(self):
        try:
            self.instance = vlc.Instance('--verbose=-1')
            self.player = self.instance.media_player_new()
            self.get_volume()
            # add avent for tittle change
            self.events = self.player.event_manager()
            self.events.event_attach(
                vlc.EventType.MediaParsedChanged, self.ParseReceived)
        except Exception as e:
            logging.critical(e)

    def ParseReceived(self):
        media = self.player.get_media()
        media.parse_with_options(1, 0)
        pass

    def load_station(self, station):
        """ load new station """
        try:
            # if it's playing and change must play the
            # new station otherwise pause
            if (self.is_playing and self.current_station != station):
                self.is_playing = False

            self.current_station = station
            self.player.set_mrl((station).url)
        except Exception as e:
            print(e)

    def toggle(self):
        if (self.is_playing):
            self.player.stop()
        else:
            self.player.play()
        self.is_playing = not self.is_playing

    def play(self):
        """play"""
        # Play the media
        try:
            self.player.play()
        except Exception as e:
            logging.warn(e)
        self.is_playing = True

    def get_info(self):
        """ get stream info """
        info = []

        startTime = time.time()
        waitFor = 1
        try:
            while True:
                media = self.player.get_media()
                media.parse_with_options(1, 0)

                # 0 exists
                if media.get_meta(12) and len(media.get_meta(12)) > 0 or (
                        waitFor < (time.time() - startTime)):
                    break

            info.append(media.get_meta(0) if media.get_meta(0) else '')
            info.append(media.get_meta(2) if media.get_meta(2) else '')
            info.append(media.get_meta(12) if media.get_meta(12) else '')
        except Exception as e:
            logging.warn(e)
            info = [' - ', ' - ', ' - ']

        return info

    def set_volume(self, vol):
        """ set volume """
        self.player.audio_set_volume(int(vol))

    def get_volume(self):
        """ get volume """
        if self.is_playing:
            self.volume = self.player.audio_get_volume()
            #  self.player.volume = self.player.audio_get_volume()

    def toggle_mute(self):
        self.player.audio_toggle_mute()
