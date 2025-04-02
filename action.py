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

class ActionRecorder:
    def __init__(self, gui, parent):
        self.parent = parent
        self.gui = gui
        self.key_thread = None  # Variável para armazenar a thread

    def add_key(self):
        """Captura combinações de teclas, agora com a opção de pressionar a tecla por um tempo."""
        # Mudar o texto do botão para "Gravando..." e desativar
        self.gui.add_key_btn.setText("Gravando...")
        self.gui.add_key_btn.setEnabled(False)

        # Criar e iniciar a thread para capturar teclas
        self.key_thread = KeyCaptureThread()
        self.key_thread.keys_captured.connect(self.on_keys_captured)
        self.key_thread.start()

    def on_keys_captured(self, hotkey):
        """Callback chamada quando as teclas forem capturadas."""
        if hotkey:
            self.parent.actions.append(("key", hotkey))
            self.gui.update_listbox()

        # Restaurar o botão após a captura
        self.gui.add_key_btn.setText("Clicar Tecla")
        self.gui.add_key_btn.setEnabled(True)
