from qt_core import *
from pynput import mouse

class MouseListenerThread(QThread):
    positions = Signal(list)

    def run(self):
        def on_click(x, y, button, pressed):
            if pressed and button == mouse.Button.left:
                self.positions.emit([x,y])
                listener.stop()

        listener = mouse.Listener(on_click=on_click)
        listener.start()