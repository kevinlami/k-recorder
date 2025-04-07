from qt_core import *

class MessageBoxRecorder:
    def __init__(self):
        super().__init__()

    def create_box(type, message, title, btn_yes=False, btn_no=False):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)

        # Define o ícone
        if type == 'warning':
            msg_box.setIcon(QMessageBox.Warning)
        elif type == 'info':
            msg_box.setIcon(QMessageBox.Information)
        elif type == 'error':
            msg_box.setIcon(QMessageBox.Critical)

        # Só define botões personalizados se necessário
        if btn_yes or btn_no:
            buttons = QMessageBox.NoButton
            if btn_yes:
                buttons |= QMessageBox.Yes
            if btn_no:
                buttons |= QMessageBox.No
            msg_box.setStandardButtons(buttons)
        # Senão, mantém o padrão (QMessageBox.Ok + X no canto)

        # Estilo
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #2d2d30;
            }
            QLabel {
                color: white;
                font-size: 14px;
                font-family: Arial;
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
        """)

        return msg_box.exec()
