import sys
import os
import time
import json
import cv2
import numpy as np
import pyautogui

from qt_core import *
from gui import UI_MainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.is_running = False
        self.actions = []
        self.loop_var = False
        self.current_index = 0

        self.setWindowTitle("K Recorder")

        self.ui = UI_MainWindow()
        self.ui.setup_ui(self)

        self.show()

    def toggle_macro(self):
        """Alterna entre iniciar e parar o macro."""
        if not self.is_running:
            self.start_macro()
        else:
            self.stop_macro()

    def start_macro(self):
        """Inicia o macro a partir da ação selecionada."""
        if not self.actions:
            return

        selected_items = self.ui.actions_listbox.selectedIndexes()
        self.current_index = selected_items[0].row() if selected_items else 0

        self.is_running = True
        self.ui.toggle_btn.setIcon(self.ui.stop_icon)  # Muda o ícone para Stop
        self.execute_next_action()

    def stop_macro(self):
        """Para a execução do macro."""
        self.is_running = False
        self.ui.toggle_btn.setIcon(self.ui.play_icon)  # Muda o ícone para Play

    def find_image_with_opencv(self, template_path, screenshot=None, threshold=0.8):
        """
        Encontra uma imagem na tela usando OpenCV.
        :param template_path: Caminho da imagem de referência.
        :param screenshot: Captura de tela (opcional).
        :param threshold: Limiar de correspondência (0 a 1).
        :return: Coordenadas da imagem encontrada ou None.
        """
        try:
            template_path = os.path.normpath(template_path)
            if not os.path.exists(template_path):
                raise FileNotFoundError(f"Arquivo não encontrado: {template_path}")

            template = cv2.imread(template_path, cv2.IMREAD_COLOR)
            if template is None:
                raise ValueError(f"Não foi possível carregar a imagem: {template_path}")

            if screenshot is None:
                screenshot = pyautogui.screenshot()
                screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

            result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(result)

            return max_loc if max_val >= threshold else None
        except Exception as e:
            print(f"Erro ao buscar imagem com OpenCV: {e}")
            return None

    def run_macro(self):
        """Executa as ações do macro."""
        if not self.actions:
            return

        selected_items = self.ui.actions_listbox.selectedIndexes()
        start_index = selected_items[0].row() if selected_items else 0

        self.is_running = True
        self.current_index = start_index
        self.execute_next_action()

    def execute_next_action(self):
        """Executa a ação atual e avança para a próxima."""
        if not self.is_running:
            self.stop_macro()
            return

        if self.current_index >= len(self.actions):
            if self.loop_var:
                self.current_index = 0
            else:
                self.stop_macro()
                return

        action, value = self.actions[self.current_index]

        self.ui.actions_listbox.clearSelection()
        self.ui.actions_listbox.setCurrentRow(self.current_index)

        should_skip_next = False

        if action == "key":
            keys = value.split('+')
            pyautogui.hotkey(*keys)

        elif action == "press_key":
            key, press_time = value
            start_time = time.time()
            while time.time() - start_time < press_time / 1000:
                pyautogui.press(key)
                time.sleep(0.05)

        elif action == "wait":
            self.current_index += 1
            QTimer.singleShot(int(value), self.execute_next_action)
            return

        elif action == "click":
            pyautogui.click(button=value)

        elif action == "move":
            pyautogui.moveTo(*value)

        elif action == "image_check":
            image_path = os.path.normpath(value)
            if os.path.exists(image_path) and os.access(image_path, os.R_OK):
                found = False
                for _ in range(3):  # Tenta até 3 vezes
                    location = self.find_image_with_opencv(image_path, threshold=0.9)
                    if location:
                        found = True
                        time.sleep(0.5)
                        pyautogui.moveTo(location[0] + 10, location[1] + 10)
                        break  
                    time.sleep(0.2)

                if not found:
                    should_skip_next = True  

        self.current_index += 1

        if should_skip_next and self.current_index < len(self.actions):
            next_action, next_value = self.actions[self.current_index]

            if next_action == "group_start":
                group_name = next_value
                while self.current_index < len(self.actions) and self.actions[self.current_index] != ["group_end", group_name]:
                    self.current_index += 1
                self.current_index += 1  
            else:
                self.current_index += 1  

        QTimer.singleShot(200, self.execute_next_action)  

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
