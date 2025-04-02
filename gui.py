from qt_core import *
from command import CommandRecorder
from action import ActionRecorder
import os

class UI_MainWindow(object):
    def setup_ui(self, parent):
        if not parent.objectName():
            parent.setObjectName("MainWindow")

        self.parent = parent

        play_pixmap = QPixmap("play_icon.png").scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.play_icon = QIcon(play_pixmap)

        stop_pixmap = QPixmap("stop_icon.png").scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.stop_icon = QIcon(stop_pixmap)

        self.command = CommandRecorder(self, parent)
        self.action = ActionRecorder(self, parent)

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

        self.create_command_list()
        self.create_actions()

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
        self.main_content_layout.setSpacing(10)

        # Lista de ações
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

        # Frame para botões de controle
        self.move_buttons_frame = QFrame()
        self.move_buttons_layout = QHBoxLayout(self.move_buttons_frame)
        self.move_buttons_layout.setSpacing(10)

        # Botões
        self.remove_btn = QPushButton("🗑 Remover")
        self.remove_btn.setStyleSheet("background-color: #d9534f; color: white; font-weight: bold;")
        self.remove_btn.clicked.connect(self.command.remove_item)

        self.move_up_btn = QPushButton("🔼 Cima")
        self.move_up_btn.setStyleSheet("background-color: #0275d8; color: white; font-weight: bold;")
        self.move_up_btn.clicked.connect(self.command.move_up)

        self.move_down_btn = QPushButton("🔽 Baixo")
        self.move_down_btn.setStyleSheet("background-color: #0275d8; color: white; font-weight: bold;")
        self.move_down_btn.clicked.connect(self.command.move_down)

        self.duplicate_btn = QPushButton("📄 Duplicar")
        self.duplicate_btn.setStyleSheet("background-color: #f0ad4e; color: white; font-weight: bold;")
        self.duplicate_btn.clicked.connect(self.command.duplicate_items)

        self.reset_btn = QPushButton("🔄 Resetar")
        self.reset_btn.setStyleSheet("background-color: #5bc0de; color: white; font-weight: bold;")
        self.reset_btn.clicked.connect(self.command.reset_macro)

        # Adicionando os botões ao layout
        self.move_buttons_layout.addWidget(self.remove_btn)
        self.move_buttons_layout.addWidget(self.move_up_btn)
        self.move_buttons_layout.addWidget(self.move_down_btn)
        self.move_buttons_layout.addWidget(self.duplicate_btn)
        self.move_buttons_layout.addWidget(self.reset_btn)

        # Adicionando o frame ao layout principal
        self.main_content_layout.addWidget(self.move_buttons_frame)

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
        self.loop_checkbox.setChecked(False)
        self.loop_checkbox.setStyleSheet("color: white;")
        self.controls_layout.addWidget(self.loop_checkbox)

        # Botão de Play/Stop sem fundo branco
        self.toggle_btn = QPushButton()
        self.toggle_btn.setIcon(self.play_icon)
        self.toggle_btn.setIconSize(QSize(64, 64))  # Define o tamanho do ícone
        self.toggle_btn.setStyleSheet("background-color: transparent; border: none; padding: 5px;")
        self.toggle_btn.clicked.connect(parent.toggle_macro)

        self.controls_layout.addWidget(self.toggle_btn)

        # Adiciona os controles ao layout do cabeçalho
        self.header_layout.addWidget(self.controls_widget)

        # Adiciona o cabeçalho ao layout principal
        self.main_layout.addWidget(self.top_menu)

    def create_actions(self):
        """Cria a área de ações."""
        # Frame para botões de ação
        self.action_buttons_frame = QFrame()
        self.action_buttons_frame.setStyleSheet("background-color: #282a36")

        self.action_buttons_layout = QVBoxLayout(self.action_buttons_frame)
        self.action_buttons_layout.setContentsMargins(10, 10, 10, 10)
        self.action_buttons_layout.setSpacing(5)

        # Botões de ação
        self.add_key_btn = QPushButton("Clicar Tecla")
        self.add_key_btn.clicked.connect(self.action.add_key)
        self.action_buttons_layout.addWidget(self.add_key_btn)

        self.press_key_btn = QPushButton("Pressionar Tecla")
        self.press_key_btn.clicked.connect(self.action.add_press_key)
        self.action_buttons_layout.addWidget(self.press_key_btn)

        self.wait_btn = QPushButton("Adicionar Espera")
        self.wait_btn.clicked.connect(self.action.add_wait)
        self.action_buttons_layout.addWidget(self.wait_btn)

        self.add_click_btn = QPushButton("Adicionar Clique")
        self.add_click_btn.clicked.connect(self.action.add_click)
        self.action_buttons_layout.addWidget(self.add_click_btn)

        self.move_mouse_btn = QPushButton("Mover Mouse")
        self.move_mouse_btn.clicked.connect(self.action.move_mouse)
        self.action_buttons_layout.addWidget(self.move_mouse_btn)

        self.add_image_btn = QPushButton("Verificar Imagem")
        #self.add_image_btn.clicked.connect(self.action.add_image_check)
        self.action_buttons_layout.addWidget(self.add_image_btn)

        self.add_group_btn = QPushButton("Adicionar Grupo")
        #self.add_group_btn.clicked.connect(self.action.add_group)
        self.action_buttons_layout.addWidget(self.add_group_btn)

        self.content_layout.addWidget(self.action_buttons_frame)

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
        