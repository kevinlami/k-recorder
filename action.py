from qt_core import *
from pynput import mouse
from overlay_selection import OverlaySelection
from input_dialog import InputDialogRecorder
from button_dialog import KeyValueOptionDialogRecorder
import keyboard
import pyautogui
import threading
import sys

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

class MouseListenerThread(QThread):
    positions = Signal(list)

    def run(self):
        def on_click(x, y, button, pressed):
            if pressed and button == mouse.Button.left:
                self.positions.emit([x,y])
                listener.stop()

        listener = mouse.Listener(on_click=on_click)
        listener.start()

class ActionRecorder():
    def __init__(self, gui, parent):
        super().__init__()
        self.parent = parent
        self.gui = gui
        self.key_thread = None

    def add_key(self, index=False):
        self.gui.add_key_btn.setText("Gravando...")
        self.gui.add_key_btn.setEnabled(False)

        self.key_thread = KeyCaptureThread()
        self.key_thread.index = index  
        self.key_thread.keys_captured.connect(self.on_keys_captured)
        self.key_thread.start()

    def on_keys_captured(self, hotkey):
        index = self.key_thread.index
        if hotkey:
            if index is not False and 0 <= index < len(self.parent.actions):
                self.parent.actions[index] = ["key", hotkey]
            else:
                self.parent.actions.append(["key", hotkey])

            self.gui.update_listbox()

        self.gui.add_key_btn.setText("Clicar Tecla")
        self.gui.add_key_btn.setEnabled(True)

    def add_press_key(self, index=False):
        """Captura a tecla a ser pressionada e por quanto tempo em milissegundos."""
        press_time, ok = InputDialogRecorder.get_int(
            self.gui.controls_widget,
            "Tempo de Pressão",
            "Digite o tempo em milissegundos que a tecla ficará pressionada:",
            value=200,
            min_value=0,
            max_value=10000
        )
        
        if ok:
            self.gui.press_key_btn.setText("Gravando...")
            self.gui.press_key_btn.setEnabled(False)

            # Criar e iniciar a thread para capturar a tecla
            self.key_thread = PressKeyCaptureThread(press_time)
            self.key_thread.index = index
            self.key_thread.keys_captured.connect(self.on_press_key_captured)
            self.key_thread.start()

    def on_press_key_captured(self, hotkey, press_time):
        index = self.key_thread.index
        if hotkey:
            if index is not False and 0 <= index < len(self.parent.actions):
                self.parent.actions[index] = (["press_key", (hotkey, press_time)])
            else:
                self.parent.actions.append(["press_key", (hotkey, press_time)])
            self.gui.update_listbox()

        # Restaurar o botão após a captura
        self.gui.press_key_btn.setText("Pressionar Tecla")
        self.gui.press_key_btn.setEnabled(True)

    def add_wait(self, index=False):
        wait_time, ok = InputDialogRecorder.get_int(
            self.gui.controls_widget,
            "Adicionar Espera",
            "Digite o tempo em milissegundos:",
            value=200,
            min_value=1
        )

        if ok and wait_time:
            if index is not False and 0 <= index < len(self.parent.actions):
                self.parent.actions[index] = (["wait", wait_time])
            else:
                self.parent.actions.append(["wait", wait_time])
            self.gui.update_listbox()

    def add_click(self, index=False):
        click_type, ok = KeyValueOptionDialogRecorder.get_option(
            "Selecionar Clique",
            {
                "left": "Clique Esquerdo",
                "middle": "Clique do Meio",
                "right": "Clique Direito"
            },
            self.gui.controls_widget
        )

        if ok:
            if click_type in ["left", "middle", "right"]:
                if index is not False and 0 <= index < len(self.parent.actions):
                    self.parent.actions[index] = (["click", click_type])
                else:
                    self.parent.actions.append(["click", click_type])
                self.gui.update_listbox()

    def move_mouse(self, index=False):
        """Aguarda um clique do usuário e captura a posição do mouse."""
        self.gui.move_mouse_btn.setText("Clique para gravar")
        self.gui.move_mouse_btn.setDisabled(True)

        self.mouse_listener = MouseListenerThread()
        self.mouse_listener.index = index
        self.mouse_listener.positions.connect(self.on_move_mouse)
        self.mouse_listener.start()

    def on_move_mouse(self, positions):
        x, y = positions
        index = self.mouse_listener.index
        if index is not False and 0 <= index < len(self.parent.actions):
            self.parent.actions[index] = (["move", (x, y)])
        else:
            self.parent.actions.append(["move", (x, y)])
        self.gui.update_listbox()
        self.gui.move_mouse_btn.setText("Mover Mouse")
        self.gui.move_mouse_btn.setDisabled(False)

    def add_image_check(self, index=False):
        self.overlay = OverlaySelection()
        self.overlay.index = index
        self.overlay.region_selected.connect(self.capture_image)
        self.overlay.show_overlay()

    def capture_image(self, region):
        file_path, _ = QFileDialog.getSaveFileName(None, "Salvar Imagem", "", "PNG Files (*.png)")
        
        if file_path:
            self.capture_thread = ImageCaptureThread(region, file_path)
            self.capture_thread.image_saved.connect(self.add_image_to_list)
            self.capture_thread.start()

    def add_image_to_list(self, image_path):
        index = self.overlay.index
        if index is not False and 0 <= index < len(self.parent.actions):
            self.parent.actions[index] = (["image_check", image_path])
        else:
            self.parent.actions.append(["image_check", image_path])
        self.gui.update_listbox()

    def add_group(self):
        """Adiciona um novo grupo em torno dos itens selecionados ou ao final da lista."""
        group_name, ok = InputDialogRecorder.get_text(None, "Nome do Grupo", "Digite o nome do grupo:")
        if not ok or not group_name:
            return  # Se o usuário cancelar ou não digitar nada, não faz nada.

        # Obtém os índices selecionados no QListWidget (em PySide6)
        selected_indices = sorted([index.row() for index in self.gui.actions_listbox.selectedIndexes()])
        
        if selected_indices:
            start_index = selected_indices[0]
            end_index = selected_indices[-1] + 1  # Ajusta para incluir o último item
            
            # Insere o grupo nos índices correspondentes (usando self.parent no lugar de self.main)
            self.parent.actions.insert(start_index, ["group_start", group_name])
            self.parent.actions.insert(end_index + 1, ["group_end", group_name])
        else:
            # Se não houver itens selecionados, adiciona um grupo vazio no final
            self.parent.actions.append(["group_start", group_name])
            self.parent.actions.append(["group_end", group_name])
        
        self.gui.update_listbox()

    def edit_group(self, index=False):
        group_name, ok = InputDialogRecorder.get_text(None, "Nome do Grupo", "Digite o nome do grupo:")
        if not ok or not group_name:
            return

        group_type, group_value = self.parent.actions[index]
        for group_end_index, (action, value) in enumerate(self.parent.actions):
            if action == 'group_end' and value == group_value:
                self.parent.actions[index] = ["group_start", group_name]
                self.parent.actions[group_end_index] = ["group_end", group_name]
                self.gui.update_listbox()
                return