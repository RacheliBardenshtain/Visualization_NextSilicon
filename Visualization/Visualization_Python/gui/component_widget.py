from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

from entities.component import Component
from utils.constants import OBJECT_COLORS, TID
from typing import Optional

from gui.log_colors_dialog import LogColorDialog
from gui.packets_colors import get_colors_by_tids


class ComponentWidget(QWidget):
    def __init__(self, component: Component, type_name: str,
                 parent: Optional[QWidget] = None) -> None:
        # Initialize with component, type_name, and optional parent widget
        super().__init__(parent)
        self.type_name = type_name
        self.component = component
        self.comp_tids = self.component.get_attribute_from_active_logs(TID)
        self.colors = get_colors_by_tids(self.comp_tids)  # Fetch colors based on TIDs
        self.initUI()

    def initUI(self) -> None:
        # Set up the user interface
        border_color = OBJECT_COLORS.get(self.type_name, 'black')
        background_color = 'white'
        if self.colors:
            background_color = self.colors[0]

        self.setStyleSheet(
            f'background-color: {background_color}; border: 2.5px solid {border_color}; padding: 0px; border-radius: 5px;')

        layout = QVBoxLayout()
        label = QLabel(self.type_name)
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        self.setLayout(layout)

        self.setCursor(Qt.ForbiddenCursor)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.RightButton:
            self.show_logs()  # Show logs on right-click

    def show_logs(self) -> None:
        # Show log dialog
        dialog = LogColorDialog(self.component, "Component Logs", self)
        dialog.exec_()
