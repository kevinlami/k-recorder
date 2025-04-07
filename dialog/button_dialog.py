from qt_core import *

class KeyValueOptionDialog(QDialog):
    def __init__(self, title: str, options: dict, parent: QWidget = None):
        super().__init__(parent if isinstance(parent, QWidget) else None)
        self.setWindowTitle(title)
        self.setStyleSheet("""
            QDialog {
                background-color: #2d2d30;
                color: white;
                font-size: 14px;
                font-family: Arial;
            }
            QPushButton {
                background-color: #4a4a4f;
                color: white;
                padding: 6px 12px;
                border-radius: 4px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #5a5a5f;
            }
            QPushButton:pressed {
                background-color: #3a3a3f;
            }
        """)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setFixedSize(280, 150)

        self.selected_key = None

        layout = QVBoxLayout()
        for key, label in options.items():
            button = QPushButton(label)
            button.clicked.connect(lambda checked=False, k=key: self.select(k))
            layout.addWidget(button)

        self.setLayout(layout)

    def select(self, key):
        self.selected_key = key
        self.accept()

class KeyValueOptionDialogRecorder:
    @staticmethod
    def get_option(title: str, options: dict, parent: QWidget = None):
        if not isinstance(parent, QWidget):
            parent = None

        dialog = KeyValueOptionDialog(title, options, parent)
        result = dialog.exec()
        return dialog.selected_key, result == QDialog.Accepted
