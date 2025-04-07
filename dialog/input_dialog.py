from qt_core import *

class InputDialogRecorder:
    @staticmethod
    def get_int(parent, title, label, value=0, min_value=0, max_value=10000):
        """Abre um QInputDialog estilizado para entrada de número inteiro."""
        dialog = QInputDialog(parent)
        dialog.setWindowTitle(title)
        dialog.setLabelText(label)
        dialog.setInputMode(QInputDialog.IntInput)
        dialog.setIntRange(min_value, max_value)
        dialog.setIntValue(value)

        dialog.setStyleSheet(InputDialogRecorder._style())
        ok = dialog.exec()
        return dialog.intValue(), bool(ok)

    @staticmethod
    def get_text(parent, title, label, default_text=""):
        """Abre um QInputDialog estilizado para entrada de texto."""
        dialog = QInputDialog(parent)
        dialog.setWindowTitle(title)
        dialog.setLabelText(label)
        dialog.setInputMode(QInputDialog.TextInput)
        dialog.setTextValue(default_text)

        dialog.setStyleSheet(InputDialogRecorder._style())
        ok = dialog.exec()
        return dialog.textValue(), bool(ok)

    @staticmethod
    def _style():
        return """
            QInputDialog {
                background-color: #2d2d30;
            }
            QLabel {
                color: white;
                font-size: 14px;
                background-color: #2d2d30;
            }
            QLineEdit {
                background-color: #3a3a3d;
                color: white;
                padding: 4px;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton {
                background-color: #4a4a4f;
                color: white;
                padding: 6px 12px;
                border-radius: 4px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #5a5a5f;
            }
            QPushButton:pressed {
                background-color: #3a3a3f;
            }
        """
