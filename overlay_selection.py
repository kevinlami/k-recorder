from qt_core import *

class OverlaySelection(QWidget):
    region_selected = Signal(QRect)
    def __init__(self, parent=None):
        super().__init__(parent)

        self.start_pos = None
        self.end_pos = None

        # 🔹 Adiciona um layout para garantir que o Qt desenhe a janela
        layout = QVBoxLayout(self)
        label = QLabel("Overlay Ativo", self)
        label.setStyleSheet("color: white; font-size: 20px;")
        layout.addWidget(label)

        # 🔹 Botão para fechar o overlay
        self.close_btn = QPushButton("Fechar Overlay", self)
        self.close_btn.clicked.connect(self.close)
        layout.addWidget(self.close_btn)

        self.setLayout(layout)

    def show_overlay(self):
        self.setStyleSheet("background-color: rgba(255, 0, 0, 100);")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(0.3)
        self.showFullScreen()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        if self.start_pos:
            self.end_pos = event.globalPos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.start_pos:
            self.end_pos = event.globalPos()
            rect = QRect(self.start_pos, self.end_pos).normalized()
            self.region_selected.emit(rect)
            self.close()

    def paintEvent(self, event):
        if self.start_pos and self.end_pos:
            painter = QPainter(self)
            painter.setPen(QPen(Qt.red, 2))
            painter.drawRect(QRect(self.start_pos, self.end_pos))
