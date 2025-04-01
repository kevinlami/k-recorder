import sys
import os

from qt_core import *
from gui6 import UI_MainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.is_running = False
        self.actions = []
        self.loop_var = False

        self.setWindowTitle("K recorder")

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
        """Inicia o macro a partir da ação selecionada na Listbox."""
        if not self.actions:
            return

        selected_indices = self.gui.actions_listbox.curselection()
        self.current_index = min(selected_indices) if selected_indices else 0

        self.is_running = True
        self.gui.toggle_btn.config(image=self.gui.stop_icon)  # Muda o ícone para Stop
        self.execute_next_action()

    def stop_macro(self):
        """Para a execução do macro."""
        self.is_running = False
        self.gui.toggle_btn.config(image=self.gui.play_icon)  # Muda o ícone para Play

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())