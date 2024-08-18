from pygame import mixer
from file_handler.load import LoadSong


class Controls():
    def __init__(self, master) -> None:
        self.master = master
        self.song = None
        self.playlist = None
        self.index = 0
        self.mode = None
        self.prev_track_count = 0
        self.paused = False

        mixer.init()
        mixer.music.set_volume(1)

    def load(self, song):
        self.song = song
        self.master.media_interface.load(song)

        if self.playlist:
            self.index = self.playlist["songs"].index(song.key)
        self.prev_track_count = 0

        mixer.music.load(song.track)
        mixer.music.play()

    def set_volume(self, volume):
        mixer.music.set_volume(volume)

    def play(self):
        mixer.music.unpause()
        self.paused = False

    def pause(self):
        mixer.music.pause()
        self.paused = True

    def play_last(self):
        if self.playlist:
            if self.prev_track_count < 3:
                self.load(self.song)
            else:
                if self.index == 0:
                    self.index == len(self.playlist)

                next_song = LoadSong(self.playlist["songs"][self.index-1])
                self.load(next_song)
        else:
            self.load(self.song)

    def play_next(self):
        if self.playlist:
            if self.index >= len(self.playlist["songs"]) - 1:
                self.index = -1

            next_song = LoadSong(self.playlist["songs"][self.index+1])
            self.load(next_song)

    def update(self):
        if not mixer.music.get_busy() and self.playlist and not self.paused:
            self.play_next()
        self.prev_track_count += 1
