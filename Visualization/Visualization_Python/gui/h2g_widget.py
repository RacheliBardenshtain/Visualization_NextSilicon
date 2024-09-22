from typing import Optional
from PyQt5.QtWidgets import (QPushButton, QVBoxLayout, QLabel, QWidget, QHBoxLayout, QAction, QMenu, QDialog,
                             QScrollArea, QTextEdit)
from PyQt5.QtCore import Qt, QSize, QPoint
from entities.component import Component
from utils.constants import OBJECT_COLORS, TID, PACKET
from gui.packets_colors import get_colors_by_tids
from entities.h2g import H2g
from gui.component_widget import ComponentWidget


class H2gWidget(QWidget):
    def __init__(self, h2g: H2g, parent: Optional[QWidget] = None) -> None:
        # Initialize the H2gWidget with H2g instance and optional parent widget.
        super().__init__(parent)
        self.h2g = h2g
        self.h2g_tids = self.h2g.get_attribute_from_active_logs(TID)  # Fetch TID attributes from logs
        self.colors = get_colors_by_tids(self.h2g_tids)  # Fetch colors for TIDs
        self.packet_messages = self.h2g.get_attribute_from_active_logs(PACKET)  # Fetch packet messages
        self.initUI()

    def initUI(self) -> None:
        # Initialize the user interface for the H2gWidget.
        self.layout = QVBoxLayout()

        self.title_label = QLabel("<b>H2G</b>")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet('border-bottom: 2px solid black; padding-bottom: 5px; margin-bottom: 10px;')
        self.layout.addWidget(self.title_label)

        # Layout for H2G components (horizontally)
        self.components_layout = QHBoxLayout()
        self.components_layout.setSpacing(10)
        self.components_layout.setContentsMargins(5, 5, 5, 5)

        # Create ComponentWidget instances for each H2G component
        self.add_component_widget(self.h2g.cbus_inj)
        self.add_component_widget(self.h2g.cbus_clt)
        self.add_component_widget(self.h2g.nfi_inj)
        self.add_component_widget(self.h2g.nfi_clt)
        self.add_component_widget(self.h2g.h2g_irqa)

        self.layout.addLayout(self.components_layout)

        # Context menu for the entire H2G widget
        self.setContextMenuPolicy(Qt.CustomContextMenu)  # Enable custom context menu
        self.customContextMenuRequested.connect(self.show_context_menu_area)

        # Close button
        self.close_button = QPushButton("Close", self)
        self.close_button.clicked.connect(self.hide_components)
        self.close_button.setCursor(Qt.PointingHandCursor)
        self.layout.addWidget(self.close_button)

        self.setLayout(self.layout)

    def add_component_widget(self, component: Component) -> None:
        # Add a ComponentWidget to the layout for the given component.
        if component:
            component_widget = ComponentWidget(component, component.type_name)
            self.components_layout.addWidget(component_widget)

    def show_context_menu_area(self, global_pos: QPoint) -> None:
        # Show a context menu when right-clicked.
        context_menu = QMenu(self)
        view_logs_action = QAction("View Logs", self)
        view_logs_action.triggered.connect(lambda: self.show_logs(None))  # Show logs for the entire area
        context_menu.addAction(view_logs_action)
        context_menu.exec_(global_pos)

    def show_logs(self, component: Optional[Component]) -> None:
        # Show a dialog with logs for the selected component or entire area.
        title = f"Logs for {component.type_name if component else 'H2G Area'}"
        dialog = QDialog(self)
        dialog.setWindowTitle(title)

        screen_size = self.screen().size()
        dialog_width = screen_size.width() // 3
        dialog_height = screen_size.height() // 3
        dialog.setFixedSize(QSize(dialog_width, dialog_height))
        dialog.setStyleSheet("background-color: white;")

        layout = QVBoxLayout(dialog)
        scroll_area = QScrollArea()
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        num_messages = len(self.packet_messages)
        num_colors = len(self.colors)

        for i in range(num_messages):
            message = self.packet_messages[i]
            color_index = i % num_colors
            color = self.colors[color_index]

            text_edit = QTextEdit()
            if isinstance(message, dict):
                text_edit.setPlainText(f"Message: {message.get('text', 'No text available')}")
            else:
                text_edit.setPlainText(f"Message: {message}")
            text_edit.setReadOnly(True)
            text_edit.setStyleSheet(f"background-color: {color}; border: 1px solid black;")
            scroll_layout.addWidget(text_edit)

        scroll_content.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_content)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)

        dialog.setLayout(layout)
        dialog.exec_()

    def show_components(self) -> None:
        # Show the H2G widget components.
        self.setVisible(True)

    def hide_components(self) -> None:
        # Hide the H2G widget components.
        self.setVisible(False)