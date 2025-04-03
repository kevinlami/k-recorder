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
        """Mostra o overlay e tenta garantir que ele fique visível."""
        self.setStyleSheet("background-color: rgba(255, 0, 0, 100);")

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(0.3)
        self.showFullScreen()
        self.activateWindow()
        self.raise_()

        QTimer.singleShot(0, QApplication.processEvents)

    def mousePressEvent(self, event):
        """Captura o clique inicial."""
        if event.button() == Qt.LeftButton:
            self.start_pos = event.globalPos()
            self.is_selecting = True
            print(f"Mouse pressionado em: {self.start_pos}")

    def mouseMoveEvent(self, event):
        """Atualiza a área enquanto o usuário arrasta."""
        if self.is_selecting:
            self.end_pos = event.globalPos()
            print(f"Movendo para: {self.end_pos}")
            self.update()

    def mouseReleaseEvent(self, event):
        """Finaliza a seleção e emite a região capturada."""
        if event.button() == Qt.LeftButton and self.is_selecting:
            self.is_selecting = False
            self.end_pos = event.globalPos()
            print(f"Mouse solto em: {self.end_pos}")

            if self.start_pos and self.end_pos:
                rect = QRect(self.start_pos, self.end_pos).normalized()
                print("Região selecionada:", rect)
                self.region_selected.emit(rect)

            self.close()

    def paintEvent(self, event):
        """Desenha o retângulo de seleção."""
        if self.start_pos and self.end_pos:
            painter = QPainter(self)
            pen = QPen(Qt.red, 2, Qt.SolidLine)
            painter.setPen(pen)
            painter.drawRect(QRect(self.start_pos, self.end_pos))
