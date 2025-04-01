from qt_core import *
from command6 import CommandRecorder
import os

class UI_MainWindow(object):
    def setup_ui(self, parent):
        if not parent.objectName():
            parent.setObjectName("MainWindow")

        self.parent = parent
        self.command = CommandRecorder(self, parent)

        parent.resize(700, 600)
        parent.setMinimumSize(700, 600)

        self.central_frame = QFrame()

        self.main_layout = QVBoxLayout(self.central_frame)
        self.main_layout.setContentsMargins(0,0,0,0)
        self.main_layout.setSpacing(0)

        self.content = QFrame()
        self.content.setStyleSheet("background-color: #282a36")

        self.content_layout = QHBoxLayout(self.content)
        self.content_layout.setContentsMargins(0,0,0,0)
        self.content_layout.setSpacing(0)

        self.left_menu = QFrame()
        self.left_menu.setStyleSheet("background-color: red")
        self.left_menu.setMaximumWidth(75)
        self.left_menu.setMinimumWidth(75)

        self.create_command_list()

        self.content_layout.addWidget(self.left_menu)
        self.content_layout.addWidget(self.main_content)

        self.create_menu(parent)
        self.create_header(parent)

        self.main_layout.addWidget(self.content)

        parent.setCentralWidget(self.central_frame)

    def create_menu(self, parent):
        menubar = parent.menuBar()  # Agora pega a barra de menu da MainWindow

        # Menu "Arquivo"
        file_menu = menubar.addMenu("Arquivo")

        save_action = QAction("Salvar Macros", parent)  # Corrigido
        save_action.triggered.connect(self.command.save_macros)
        file_menu.addAction(save_action)

        load_action = QAction("Carregar Macros", parent)  # Corrigido
        load_action.triggered.connect(self.command.load_macros)
        file_menu.addAction(load_action)

        file_menu.addSeparator()

        exit_action = QAction("Sair", parent)  # Corrigido
        exit_action.triggered.connect(parent.close)
        file_menu.addAction(exit_action)

        # Menu "Macro"
        macro_menu = menubar.addMenu("Macro")

        run_action = QAction("▶ Rodar Macro", parent)  # Corrigido
        run_action.setShortcut(QKeySequence("F5"))
        run_action.triggered.connect(parent.start_macro)
        macro_menu.addAction(run_action)

        stop_action = QAction("■ Parar Macro", parent)  # Corrigido
        stop_action.setShortcut(QKeySequence("F6"))
        stop_action.triggered.connect(parent.stop_macro)
        macro_menu.addAction(stop_action)

    def create_command_list(self):
        self.main_content = QFrame()
        self.main_content.setStyleSheet("background-color: #282a36")

        self.main_content_layout = QVBoxLayout(self.main_content)
        self.main_content_layout.setContentsMargins(10, 10, 10, 10)
        self.main_content_layout.setSpacing(0)

        self.actions_listbox = QListWidget()
        self.actions_listbox.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.actions_listbox.setStyleSheet("""
            QListWidget {
                background-color: #f0f0f0;
                border: 1px solid #ccc;
                padding: 5px;
                font-size: 14px;
            }
            QListWidget::item {
                padding: 5px;
                border-bottom: 1px solid #ddd;
            }
            QListWidget::item:selected {
                background-color: #d0d0ff;
                color: black;
            }
        """)

        self.main_content_layout.addWidget(self.actions_listbox)

    def create_header(self, parent): 
        """Cria o cabeçalho no PySide6."""

        # Criando um widget para conter o cabeçalho
        self.top_menu = QFrame()
        self.top_menu.setStyleSheet("background-color: #44478a")
        self.top_menu.setMaximumHeight(75)
        self.top_menu.setMinimumHeight(75)

        self.header_layout = QHBoxLayout(self.top_menu)
        self.header_layout.setContentsMargins(10, 5, 10, 5)

        # Título alinhado à esquerda
        self.title_label = QLabel("K Recorder")
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: white;")
        self.header_layout.addWidget(self.title_label)

        # Adiciona um espaço flexível para empurrar os botões para a direita
        self.header_layout.addStretch()

        # Criando um widget para conter os botões de controle
        self.controls_widget = QWidget()
        self.controls_layout = QHBoxLayout(self.controls_widget)
        self.controls_layout.setContentsMargins(0, 0, 0, 0)

        # Checkbox de Loop Infinito
        self.loop_checkbox = QCheckBox("Loop Infinito")
        self.loop_checkbox.setChecked(parent.loop_var)
        self.loop_checkbox.setStyleSheet("color: white;")
        self.controls_layout.addWidget(self.loop_checkbox)

        # Carregando ícones para Play e Stop com tamanho dobrado (64x64)
        play_pixmap = QPixmap("play_icon.png").scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        play_icon = QIcon(play_pixmap)

        # Botão de Play/Stop sem fundo branco
        self.toggle_btn = QPushButton()
        self.toggle_btn.setIcon(play_icon)
        self.toggle_btn.setIconSize(QSize(64, 64))  # Define o tamanho do ícone
        self.toggle_btn.setStyleSheet("background-color: transparent; border: none; padding: 5px;")
        self.toggle_btn.clicked.connect(parent.toggle_macro)

        self.controls_layout.addWidget(self.toggle_btn)

        # Adiciona os controles ao layout do cabeçalho
        self.header_layout.addWidget(self.controls_widget)

        # Adiciona o cabeçalho ao layout principal
        self.main_layout.addWidget(self.top_menu)

    def update_listbox(self):
        """Atualiza o QListWidget sem perder a posição do scroll."""
        # Salva a posição atual do scroll
        scroll_pos = self.actions_listbox.verticalScrollBar().value()

        # Limpa a lista
        self.actions_listbox.clear()

        # Atualiza os itens
        for action, value in self.parent.actions:
            match action:
                case "key":
                    item_text = f"Pressionar: {value}"
                case "press_key":
                    key, press_time = value
                    item_text = f"Pressionar {key} por {press_time} ms"
                case "wait":
                    item_text = f"Esperar {value} ms"
                case "click":
                    item_text = f"Clique {value}"
                case "move":
                    item_text = f"Mover mouse para {value}"
                case "image_check":
                    item_text = f"Verificar Imagem: {os.path.basename(value)}"
                case "group_start":
                    item_text = f"📂 Grupo: {value}"
                case "group_end":
                    item_text = f"📁 Fim do Grupo: {value}"
            
            # Adiciona o item à lista
            self.actions_listbox.addItem(item_text)

        # Restaura a posição do scroll
        self.actions_listbox.verticalScrollBar().setValue(scroll_pos)
        