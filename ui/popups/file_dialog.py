from PyQt6.QtWidgets import QFileDialog


class Selector(QFileDialog):
    def __init__(self) -> None:
        super().__init__()

        self.setModal(True)
        self.setOption(QFileDialog.Option.ReadOnly, True)

        self.image_exts = "*.jpg *.jpeg *.png *.webp *.svg"
        self.song_exts = "*.mp3 *.wav *.ogg"

    def get_file(self, type):
        if type == "image":
            ext = self.image_exts
        elif type == "song":
            ext = self.song_exts
        return self.getOpenFileName(filter=ext)
