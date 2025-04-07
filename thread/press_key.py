from qt_core import *
import keyboard

class PressKeyCaptureThread(QThread):
    keys_captured = Signal(str, int)  # Sinal para enviar a tecla capturada e o tempo

    def __init__(self, press_time):
        super().__init__()
        self.press_time = press_time

    def run(self):
        """Captura a tecla a ser pressionada e retorna junto com o tempo."""
        recorded_keys = []  # Lista para manter a ordem
        pressed_keys = set()  # Controla teclas pressionadas

        while True:
            event = keyboard.read_event()

            if event.event_type == "down":
                if event.name not in pressed_keys:
                    recorded_keys.append(event.name)  # Adiciona na ordem
                    pressed_keys.add(event.name)
            elif event.event_type == "up":
                if event.name in pressed_keys:
                    pressed_keys.remove(event.name)

            # Sai quando todas as teclas forem soltas
            if not pressed_keys:
                break

        hotkey = "+".join(recorded_keys)
        if hotkey:
            self.keys_captured.emit(hotkey, self.press_time)  # Emite o sinal