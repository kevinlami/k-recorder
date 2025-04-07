from qt_core import *
import keyboard

class KeyCaptureThread(QThread):
    keys_captured = Signal(str)  # Sinal para enviar as teclas capturadas

    def run(self):
        """Captura combinações de teclas em uma thread separada."""
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
            self.keys_captured.emit(hotkey)  # Emite o sinal com a tecla capturada