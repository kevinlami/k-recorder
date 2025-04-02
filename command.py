from qt_core import *
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
    
    def remove_item(self):
        """Remove itens selecionados, considerando grupos."""
        selected_indices = sorted([index.row() for index in self.gui.actions_listbox.selectedIndexes()], reverse=True)

        for index in selected_indices:
            if 0 <= index < len(self.parent.actions):
                if self.parent.actions[index][0] == "group_start":
                    # Remover tudo até encontrar "group_end"
                    group_name = self.parent.actions[index][1]
                    while index < len(self.parent.actions) and self.parent.actions[index] != ["group_end", group_name]:
                        self.parent.actions.pop(index)
                    self.parent.actions.pop(index)  # Remove também "group_end"
                else:
                    self.parent.actions.pop(index)
        
        self.gui.update_listbox()

    def reset_macro(self):
        """Reseta todos os dados do macro."""
        try:
            # Limpa a lista de ações
            self.parent.actions.clear()

            # Limpa a lista de ações exibida na interface
            self.gui.actions_listbox.clear()
        except Exception as e:
            QMessageBox.critical(None, "Erro", f"Erro ao resetar o macro: {e}")

    def move_up(self):
        """Move ações ou grupos selecionados para cima."""
        selected_indices = sorted([index.row() for index in self.gui.actions_listbox.selectedIndexes()])
        if not selected_indices or selected_indices[0] == 0:
            return

        for index in selected_indices:
            if 0 < index < len(self.parent.actions):
                self.parent.actions[index - 1], self.parent.actions[index] = self.parent.actions[index], self.parent.actions[index - 1]

        self.gui.update_listbox()

        # Atualiza a seleção após mover
        self.gui.actions_listbox.clearSelection()
        for index in selected_indices:
            self.gui.actions_listbox.setCurrentRow(index - 1)
            self.gui.actions_listbox.selectionModel().select(
                self.gui.actions_listbox.model().index(index - 1, 0),
                QItemSelectionModel.Select
            )

    def move_down(self):
        """Move ações ou grupos selecionados para baixo."""
        selected_indices = sorted([index.row() for index in self.gui.actions_listbox.selectedIndexes()], reverse=True)
        if not selected_indices or selected_indices[-1] == len(self.parent.actions) - 1:
            return

        for index in selected_indices:
            if index < len(self.parent.actions) - 1:
                self.parent.actions[index + 1], self.parent.actions[index] = self.parent.actions[index], self.parent.actions[index + 1]

        self.gui.update_listbox()

        # Atualiza a seleção após mover
        self.gui.actions_listbox.clearSelection()
        for index in selected_indices:
            self.gui.actions_listbox.setCurrentRow(index + 1)
            self.gui.actions_listbox.selectionModel().select(
                self.gui.actions_listbox.model().index(index + 1, 0),
                QItemSelectionModel.Select
            )

    def duplicate_items(self):
        """Duplica os itens selecionados e adiciona ao final da lista."""
        selected_indices = sorted([index.row() for index in self.gui.actions_listbox.selectedIndexes()])
        if not selected_indices:
            return

        new_items = []
        i = 0

        while i < len(selected_indices):
            index = selected_indices[i]
            action = self.parent.actions[index]

            if action[0] == "group_start":
                # Encontrar o índice correspondente do "group_end"
                group_name = action[1]
                end_index = index + 1

                while end_index < len(self.parent.actions) and self.parent.actions[end_index] != ["group_end", group_name]:
                    end_index += 1

                if end_index < len(self.parent.actions):
                    end_index += 1  # Incluir o "group_end" na cópia

                new_items.extend(self.parent.actions[index:end_index])  # Copia o grupo inteiro
                i = selected_indices.index(end_index - 1) + 1 if end_index - 1 in selected_indices else i + 1
            else:
                new_items.append(action)
                i += 1

        self.parent.actions.extend(new_items)
        self.gui.update_listbox()

