from typing import Optional
from PyQt5.QtCore import QSize, QPoint, Qt
from PyQt5.QtWidgets import (QPushButton, QVBoxLayout, QLabel, QWidget, QGridLayout, QTextEdit, QMenu, QAction,
                             QDialog, QScrollArea)
from entities.component import Component
from utils.constants import OBJECT_COLORS, TID, PACKET
from entities.g2h import G2h
from gui.component_widget import ComponentWidget
from gui.log_colors_dialog import LogColorDialog
from gui.packets_colors import get_colors_by_tids


class G2hWidget(QWidget):
    def __init__(self, g2h: G2h, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.g2h = g2h
        self.g2h_tids = self.g2h.get_attribute_from_active_logs(TID)
        self.colors = get_colors_by_tids(self.g2h_tids)  # Fetch colors
        self.packet_messages = self.g2h.get_attribute_from_active_logs(PACKET)  # Fetch packet messages
        self.initUI()

    # Initializing all UI elements
    def initUI(self) -> None:
        self.layout = QVBoxLayout()

        self.title_label = QLabel("<b>G2H</b>")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet('border-bottom: 2px solid black; padding-bottom: 5px; margin-bottom: 10px;')
        self.layout.addWidget(self.title_label)

        # Layout for G2H components (grid layout)
        self.components_layout = QGridLayout()
        self.components_layout.setSpacing(10)
        self.components_layout.setContentsMargins(10, 10, 10, 10)

        # Add g2h_irqa first
        if self.g2h.g2h_irqa:
            component_widget = ComponentWidget(self.g2h.g2h_irqa, self.g2h.g2h_irqa.type_name)
            self.components_layout.addWidget(component_widget, 0, 0)

        # Add EQS components
        row = 1
        col = 0
        for eq in self.g2h.eqs:
            component_widget = ComponentWidget(eq, eq.type_name)
            self.components_layout.addWidget(component_widget, row, col)
            col += 1
            if col >= 7:  # Limit columns to 3
                col = 0
                row += 1

        self.layout.addLayout(self.components_layout)

        # Close button
        self.close_button = QPushButton("Close", self)
        self.close_button.clicked.connect(self.hide_components)
        self.close_button.setStyleSheet('background-color: #d9534f; color: white; border-radius: 5px; padding: 10px;')
        self.close_button.setCursor(Qt.PointingHandCursor)
        self.layout.addWidget(self.close_button)

        self.setLayout(self.layout)
        self.setVisible(False)

    # Creating component button
    def create_component_button(self, component: Component, row: Optional[int] = None,
                                col: Optional[int] = None) -> None:
        if component is None:
            return

        color = OBJECT_COLORS.get(component.type_name, 'white')
        first_color = self.colors[0] if self.colors else 'white'  # Use the first color in the list

        button = QPushButton(component.type_name or "Unknown", self)
        button.setFixedSize(150, 50)
        button.setStyleSheet(
            f'background-color: {first_color}; border: 2px solid {color}; border-radius: 5px; padding: 10px; color: black;'
        )
        button.setContextMenuPolicy(Qt.CustomContextMenu)
        button.customContextMenuRequested.connect(
            lambda pos, comp=component: self.show_context_menu(button.mapToGlobal(pos), comp))

        if row is not None and col is not None:
            self.components_layout.addWidget(button, row, col)
        else:
            self.components_layout.addWidget(button)

    # Show the context menu
    def show_context_menu(self, global_pos: QPoint, component: Component) -> None:
        context_menu = QMenu(self)
        view_logs_action = QAction("View Logs", self)
        view_logs_action.triggered.connect(lambda: self.show_logs(component))
        context_menu.addAction(view_logs_action)
        context_menu.exec_(global_pos)

    # Show logs in a dialog
    def show_logs(self, component: Component) -> None:
        dialog = LogColorDialog(self.g2h, f"Logs for {component.type_name or 'Unknown'}", self)
        dialog.exec_()

    # Show the components
    def show_components(self) -> None:
        self.setVisible(True)

    # Hide the components
    def hide_components(self) -> None:
        self.setVisible(False)
