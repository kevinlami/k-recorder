from PySide6.QtWidgets import QMessageBox, QFileDialog
import json

class CommandRecorder:
    def __init__(self, gui, parent):
        self.parent = parent
        self.gui = gui

    def save_macros(self):
        """Salva a lista de ações em um arquivo."""
        if not self.parent.actions:
            QMessageBox.warning(self.parent, "Aviso", "Nenhuma ação para salvar!")
            return

        file_path, _ = QFileDialog.getSaveFileName(self.parent, "Salvar Macro", "", "JSON Files (*.json)")
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    json.dump(self.parent.actions, file)
                QMessageBox.information(self.parent, "Sucesso", "Macros salvos com sucesso!")
            except Exception as e:
                QMessageBox.critical(self.parent, "Erro", f"Erro ao salvar macros: {e}")

    def load_macros(self):
        """Carrega a lista de ações de um arquivo."""
        file_path, _ = QFileDialog.getOpenFileName(self.parent, "Carregar Macro", "", "JSON Files (*.json)")
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    self.parent.actions = json.load(file)
                self.gui.update_listbox()
                QMessageBox.information(self.parent, "Sucesso", "Macros carregados com sucesso!")
            except Exception as e:
                QMessageBox.critical(self.parent, "Erro", f"Erro ao carregar macros: {e}")
