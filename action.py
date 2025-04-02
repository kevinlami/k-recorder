from qt_core import *
import keyboard
from pynput import mouse

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

    def add_press_key(self):
        """Captura a tecla a ser pressionada e por quanto tempo em milissegundos."""
        press_time, ok = QInputDialog.getInt(
            self.gui.controls_widget,  # Usa um QWidget válido
            "Tempo de Pressão", 
            "Digite o tempo em milissegundos que a tecla ficará pressionada:", 
            value=200,  # Valor inicial sugerido
            minValue=0,  # Valor mínimo
            maxValue=10000,  # Valor máximo
        )
        
        if ok:
            self.gui.press_key_btn.setText("Gravando...")
            self.gui.press_key_btn.setEnabled(False)

            # Criar e iniciar a thread para capturar a tecla
            self.key_thread = PressKeyCaptureThread(press_time)
            self.key_thread.keys_captured.connect(self.on_press_key_captured)
            self.key_thread.start()

    def on_press_key_captured(self, hotkey, press_time):
        """Callback chamada quando a tecla pressionada for capturada."""
        if hotkey:
            self.parent.actions.append(("press_key", (hotkey, press_time)))
            self.gui.update_listbox()

        # Restaurar o botão após a captura
        self.gui.press_key_btn.setText("Pressionar Tecla")
        self.gui.press_key_btn.setEnabled(True)

    def add_wait(self):
        """Adiciona um tempo de espera em milissegundos."""
        wait_time, ok = QInputDialog.getInt(
            self.gui.controls_widget,
            "Adicionar Espera",
            "Digite o tempo em milissegundos:",
            value=200,  # Valor inicial sugerido
            minValue=1  # Defina um valor mínimo para evitar números negativos
        )

        if ok and wait_time:
            self.parent.actions.append(("wait", wait_time))
            self.gui.update_listbox()

    def add_click(self):
        """Adiciona um clique do mouse usando botões em vez de input, com janela centralizada."""
        
        class ClickDialog(QDialog):
            def __init__(self, parent: QWidget = None):
                super().__init__(parent)
                self.setWindowTitle("Adicionar Clique")
                self.setFixedSize(250, 100)
                
                layout = QVBoxLayout()
                self.selected_button = None

                def set_click(value):
                    self.selected_button = value
                    self.accept()  # Fecha a janela ao escolher

                # Criando botões para seleção
                for btn_text in ["Left", "Middle", "Right"]:
                    button = QPushButton(btn_text)
                    button.clicked.connect(lambda checked, b=btn_text.lower(): set_click(b))
                    layout.addWidget(button)

                self.setLayout(layout)

        dialog = ClickDialog(self.gui if isinstance(self.gui, QWidget) else None)
        if dialog.exec():
            click_type = dialog.selected_button
            if click_type in ["left", "middle", "right"]:
                self.parent.actions.append(("click", click_type))
                self.gui.update_listbox()

    def move_mouse(self):
        """Aguarda um clique do usuário e captura a posição do mouse."""
        self.gui.move_mouse_btn.setText("Clique para gravar")
        self.gui.move_mouse_btn.setDisabled(True)

        def on_click(x, y, button, pressed):
            if pressed and button == mouse.Button.left:  # Captura apenas o clique esquerdo
                self.parent.actions.append(("move", (x, y)))
                self.gui.update_listbox()
                self.gui.move_mouse_btn.setText("Mover Mouse")
                self.gui.move_mouse_btn.setDisabled(False)
                listener.stop()  # Para o listener após capturar o clique

        # Executa o listener em uma thread separada
        listener = mouse.Listener(on_click=on_click)
        listener.start()

