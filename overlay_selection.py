from qt_core import *

class OverlaySelection(QWidget):
    region_selected = Signal(QRect)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        # Inicializa os atributos de seleção
        self.start_pos = None
        self.end_pos = None
        self.is_selecting = False
        
        # Cria o label informativo sem layout para que não ocupe toda a área de clique
        self.label = QLabel("Clique e arraste para selecionar uma região.", self)
        self.label.setStyleSheet("color: white; font-size: 16px; font-weight: bold; background: transparent;")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setGeometry(10, 10, 400, 30)
        
        # Cria o botão de fechar, que ficará no topo-direita
        self.close_btn = QPushButton("X", self)
        self.close_btn.setFixedSize(30, 30)
        self.close_btn.setStyleSheet("background-color: rgba(50, 50, 50, 150); color: white; border-radius: 15px;")
        self.close_btn.clicked.connect(self.close)
        # Posição temporária; será ajustada em resizeEvent
        self.close_btn.setGeometry(0, 10, 30, 30)
    
    def show_overlay(self):
        """Exibe o overlay ocupando toda a tela com fundo cinza translúcido."""
        # Configura a janela sem borda e com fundo transparente (será pintado no paintEvent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.showFullScreen()
        self.raise_()
        self.activateWindow()
    
    def resizeEvent(self, event):
        """Ajusta a posição do label e do botão de fechar conforme o tamanho da tela."""
        self.label.setGeometry(10, 10, self.width() - 60, 30)
        self.close_btn.move(self.width() - 40, 10)
        super().resizeEvent(event)
    
    def paintEvent(self, event):
        """Pinta o fundo cinza e o retângulo de seleção (se houver)."""
        painter = QPainter(self)
        # Preenche toda a área com cinza translúcido
        painter.fillRect(self.rect(), QColor(50, 50, 50, 180))
        # Se houver uma seleção, desenha o retângulo branco
        if self.start_pos and self.end_pos:
            pen = QPen(Qt.white, 2)
            painter.setPen(pen)
            painter.drawRect(QRect(self.start_pos, self.end_pos))
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Registra a posição inicial da seleção
            self.start_pos = event.globalPos()
            self.end_pos = self.start_pos
            self.is_selecting = True
            self.update()
    
    def mouseMoveEvent(self, event):
        if self.is_selecting:
            self.end_pos = event.globalPos()
            self.update()
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.is_selecting:
            self.is_selecting = False
            self.end_pos = event.globalPos()
            if self.start_pos and self.end_pos:
                rect = QRect(self.start_pos, self.end_pos).normalized()
                self.region_selected.emit(rect)
            self.close()
