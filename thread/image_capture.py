from qt_core import *
import pyautogui

class ImageCaptureThread(QThread):
    image_saved = Signal(str)

    def __init__(self, region, file_path):
        super().__init__()
        self.region = region
        self.file_path = file_path

    def run(self):
        x, y, w, h = self.region.x(), self.region.y(), self.region.width(), self.region.height()
        image = pyautogui.screenshot(region=(x, y, w, h))
        image.save(self.file_path)
        self.image_saved.emit(self.file_path)