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

        parent.resize(800, 600)
        parent.setMinimumSize(800, 600)

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

        # Aplica stylesheet global para modernizar a interface
        self.apply_styles()

    def apply_styles(self):
        style = """
            QMainWindow { background-color: #1e1e1e; }
            QMenuBar { background-color: #333; color: white; font-size: 14px; }
            QMenuBar::item { padding: 5px 15px; }
            QMenuBar::item:selected { background-color: #444; }
            QMenu { background-color: #333; color: white; }
            QMenu::item:selected { background-color: #444; }
            QPushButton { border: none; padding: 8px 12px; border-radius: 4px; font-size: 14px; }\n"
            QPushButton:hover { background-color: #555; }\n"
            QListWidget { border: 1px solid #ccc; font-size: 14px; }\n"
            QCheckBox { font-size: 14px; color: white; }\n"
        """
        self.parent.setStyleSheet(style)

    def create_menu(self, parent):
        menubar = parent.menuBar()
        file_menu = menubar.addMenu("Arquivo")

        save_action = QAction("Salvar Macros", parent)
        save_action.triggered.connect(self.command.save_macros)
        file_menu.addAction(save_action)

        load_action = QAction("Carregar Macros", parent)
        load_action.triggered.connect(self.command.load_macros)
        file_menu.addAction(load_action)

        file_menu.addSeparator()

        exit_action = QAction("Sair", parent)
        exit_action.triggered.connect(parent.close)
        file_menu.addAction(exit_action)

        macro_menu = menubar.addMenu("Macro")
        run_action = QAction("▶ Rodar Macro", parent)
        run_action.setShortcut(QKeySequence("F5"))
        run_action.triggered.connect(parent.start_macro)
        macro_menu.addAction(run_action)

        stop_action = QAction("■ Parar Macro", parent)
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
                background-color: #6D7393;
                border: 1px solid #6D7393;
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

        # Estilo moderno para os botões
        modern_button_style = """
            QPushButton {
                background-color: [bg];
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: [bg-hover];
            }
            QPushButton:pressed {
                background-color: [bg-press];
            }
        """

        blue_button_style = modern_button_style.replace('[bg]', '#0275d8').replace('[bg-hover]', '#117CD9').replace('[bg-press]', '#117CD9')
        red_button_style = modern_button_style.replace('[bg]', '#d9534f').replace('[bg-hover]', '#D9615D').replace('[bg-press]', '#D9615D')
        yellow_button_style = modern_button_style.replace('[bg]', '#f0ad4e').replace('[bg-hover]', '#F0B35D').replace('[bg-press]', '#F0B35D')
        light_blue_button_style = modern_button_style.replace('[bg]', '#5BC0DE').replace('[bg-hover]', '#6AC3DE').replace('[bg-press]', '#6AC3DE')

        # Botões
        self.remove_btn = QPushButton("  Remover")
        self.remove_btn.setStyleSheet(red_button_style)
        self.remove_btn.setIcon(QIcon("icons/delete.svg"))
        self.remove_btn.setIconSize(QSize(18, 18))
        self.remove_btn.clicked.connect(self.command.remove_item)

        self.move_up_btn = QPushButton("  Cima")
        self.move_up_btn.setStyleSheet(blue_button_style)
        self.move_up_btn.setIcon(QIcon("icons/move_up.svg"))
        self.move_up_btn.setIconSize(QSize(18, 18))
        self.move_up_btn.clicked.connect(self.command.move_up)

        self.move_down_btn = QPushButton("  Baixo")
        self.move_down_btn.setStyleSheet(blue_button_style)
        self.move_down_btn.setIcon(QIcon("icons/move_down.svg"))
        self.move_down_btn.setIconSize(QSize(18, 18))
        self.move_down_btn.clicked.connect(self.command.move_down)

        self.duplicate_btn = QPushButton("  Duplicar")
        self.duplicate_btn.setStyleSheet(yellow_button_style)
        self.duplicate_btn.setIcon(QIcon("icons/duplicate.svg"))
        self.duplicate_btn.setIconSize(QSize(18, 18))
        self.duplicate_btn.clicked.connect(self.command.duplicate_items)

        self.reset_btn = QPushButton("  Resetar")
        self.reset_btn.setStyleSheet(light_blue_button_style)
        self.reset_btn.setIcon(QIcon("icons/reset.svg"))
        self.reset_btn.setIconSize(QSize(18, 18))
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
        """Cria um cabeçalho moderno no PySide6."""
        # Cria o QFrame do cabeçalho com gradiente
        self.top_menu = QFrame()
        self.top_menu.setFixedHeight(75)
        self.top_menu.setStyleSheet("background-color: #404147")
        
        # Layout do cabeçalho com margens e espaçamento otimizados
        self.header_layout = QHBoxLayout(self.top_menu)
        self.header_layout.setContentsMargins(20, 10, 20, 10)
        self.header_layout.setSpacing(10)
        
        # Título com fonte moderna e maior
        self.title_label = QLabel("K Recorder")
        font = QFont("Segoe UI", 20, QFont.Bold)  # Você pode trocar por outra fonte moderna instalada no sistema
        self.title_label.setFont(font)
        self.title_label.setStyleSheet("color: white;")
        self.header_layout.addWidget(self.title_label)
        
        self.header_layout.addStretch()
        
        # Widget de controles à direita
        self.controls_widget = QWidget()
        controls_layout = QHBoxLayout(self.controls_widget)
        controls_layout.setContentsMargins(0, 0, 0, 0)
        controls_layout.setSpacing(10)
        
        # Checkbox estilizado como toggle switch
        self.loop_checkbox = QCheckBox("Loop Infinito")
        self.loop_checkbox.setChecked(False)
        self.loop_checkbox.setStyleSheet("""
            QCheckBox {
                color: white;
                font-size: 16px;
            }
            QCheckBox::indicator {
                width: 15px;
                height: 15px;
                border: 3px solid #888;
            }
            QCheckBox::indicator:unchecked {
                border-radius: 10px;
                background-color: #888;
            }
            QCheckBox::indicator:checked {
                border-radius: 10px;
                background-color: #65EB6A;
            }
        """)
        controls_layout.addWidget(self.loop_checkbox)
        
        # Botão de Play/Stop com efeitos de hover e pressed
        self.toggle_btn = QPushButton()
        self.toggle_btn.setIcon(self.play_icon)
        self.toggle_btn.setIconSize(QSize(64, 64))
        self.toggle_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.2);
            }
        """)
        self.toggle_btn.clicked.connect(parent.toggle_macro)
        controls_layout.addWidget(self.toggle_btn)
        
        self.header_layout.addWidget(self.controls_widget)
        
        self.main_layout.addWidget(self.top_menu)

    def create_actions(self):
        # Cria o frame de botões de ação com fundo escuro
        self.action_buttons_frame = QFrame()
        self.action_buttons_frame.setStyleSheet("background-color: #282a36;")
        action_layout = QVBoxLayout(self.action_buttons_frame)
        action_layout.setContentsMargins(10, 10, 10, 10)
        action_layout.setSpacing(10)
        
        # Estilo moderno para os botões
        modern_button_style = """
            QPushButton {
                background-color: #3c3f41;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #505355;
            }
            QPushButton:pressed {
                background-color: #2d2f31;
            }
        """
        
        # Botão: Clicar Tecla
        self.add_key_btn = QPushButton("  Clicar Tecla")
        self.add_key_btn.setStyleSheet(modern_button_style)
        self.add_key_btn.setIcon(QIcon("icons/key.svg"))
        self.add_key_btn.setIconSize(QSize(24, 24))
        self.add_key_btn.clicked.connect(self.action.add_key)
        action_layout.addWidget(self.add_key_btn)
        
        # Botão: Pressionar Tecla
        self.press_key_btn = QPushButton("  Pressionar Tecla")
        self.press_key_btn.setStyleSheet(modern_button_style)
        self.press_key_btn.setIcon(QIcon("icons/press_key.svg"))
        self.press_key_btn.setIconSize(QSize(24, 24))
        self.press_key_btn.clicked.connect(self.action.add_press_key)
        action_layout.addWidget(self.press_key_btn)
        
        # Botão: Adicionar Espera
        self.wait_btn = QPushButton("  Adicionar Espera")
        self.wait_btn.setStyleSheet(modern_button_style)
        self.wait_btn.setIcon(QIcon("icons/wait.svg"))
        self.wait_btn.setIconSize(QSize(24, 24))
        self.wait_btn.clicked.connect(self.action.add_wait)
        action_layout.addWidget(self.wait_btn)
        
        # Botão: Adicionar Clique
        self.add_click_btn = QPushButton("  Adicionar Clique")
        self.add_click_btn.setStyleSheet(modern_button_style)
        self.add_click_btn.setIcon(QIcon("icons/mouse_click.svg"))
        self.add_click_btn.setIconSize(QSize(24, 24))
        self.add_click_btn.clicked.connect(self.action.add_click)
        action_layout.addWidget(self.add_click_btn)
        
        # Botão: Mover Mouse
        self.move_mouse_btn = QPushButton("  Mover Mouse")
        self.move_mouse_btn.setStyleSheet(modern_button_style)
        self.move_mouse_btn.setIcon(QIcon("icons/move_mouse.svg"))
        self.move_mouse_btn.setIconSize(QSize(24, 24))
        self.move_mouse_btn.clicked.connect(self.action.move_mouse)
        action_layout.addWidget(self.move_mouse_btn)
        
        # Botão: Verificar Imagem
        self.add_image_btn = QPushButton("  Verificar Imagem")
        self.add_image_btn.setStyleSheet(modern_button_style)
        self.add_image_btn.setIcon(QIcon("icons/image.svg"))
        self.add_image_btn.setIconSize(QSize(24, 24))
        self.add_image_btn.clicked.connect(self.action.add_image_check)
        action_layout.addWidget(self.add_image_btn)
        
        # Botão: Adicionar Grupo
        self.add_group_btn = QPushButton("  Adicionar Grupo")
        self.add_group_btn.setStyleSheet(modern_button_style)
        self.add_group_btn.setIcon(QIcon("icons/group.svg"))
        self.add_group_btn.setIconSize(QSize(24, 24))
        self.add_group_btn.clicked.connect(self.action.add_group)
        action_layout.addWidget(self.add_group_btn)

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
        