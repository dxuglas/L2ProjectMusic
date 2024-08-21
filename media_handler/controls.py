from pygame import mixer
from file_handler.load import LoadSong


class Controls():
    def __init__(self, master) -> None:
        """The init function for the media controller. Sets up the default 
        values so it is ready to play music. 

        Args:
            master (MainWindow): The main window it is controlling audio for. 
        """

        self.master = master 

        # Current song information
        self.song = None
        self.playlist = None
        self.index = 0
        self.paused = False
        
        # The counter to allow different modes for the previous track button
        self.prev_track_count = 0

        mixer.init()
        mixer.music.set_volume(1)

    def load(self, song):
        """Loads a song file and streams in to the users audio channels. Also
        triggers the media interface to be updated.

        Args:
            song (LoadSong): The song that needs to be loaded. 
        """

        self.song = song
        self.master.media_interface.load(song)

        # If the song is being played as a member of a playlist store its index
        if self.playlist:
            self.index = self.playlist["songs"].index(song.key)

        self.prev_track_count = 0

        mixer.music.load(song.track)
        mixer.music.play()

    def set_volume(self, volume: float):
        """Update the volume of the audio stream. 

        Args:
            volume (float): The updated volume value. 
        """

        mixer.music.set_volume(volume)

    def play(self):
        """Play the music from a paused state.
        """
        mixer.music.unpause()
        self.paused = False

    def pause(self):
        """Pause the music from a playing state.
        """
        mixer.music.pause()
        self.paused = True

    def play_last(self):
        """Play the previous track or restart the current track
        """

        # If the song being played is in a playlist.
        if self.playlist:
            # If the current song was recently loaded restart it
            if self.prev_track_count < 3:
                self.load(self.song)
            # Otherwise play the previous song in the playlsit
            else:
                if self.index == 0:
                    self.index == len(self.playlist)

                next_song = LoadSong(self.playlist["songs"][self.index-1])
                self.load(next_song)
        # Otherwise restart the current song
        else:
            self.load(self.song)

    def play_next(self):
        """Play the next song in the playlist.
        """
        if self.playlist:
            # Check for index overflow. 
            if self.index >= len(self.playlist["songs"]) - 1:
                self.index = -1

            # Load the next song.
            next_song = LoadSong(self.playlist["songs"][self.index+1])
            self.load(next_song)

    def update(self):
        """The controller update loop which listens to the mixer and queues the
        next song once the current one has been completed. 
        """
        if not mixer.music.get_busy() and self.playlist and not self.paused:
            self.play_next()
        self.prev_track_count += 1
