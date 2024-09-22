from typing import Dict, Optional

from PyQt5.QtWidgets import (QPushButton, QVBoxLayout, QLabel, QWidget, QHBoxLayout, QFrame, QMenu, QAction,
                             QDialog, QTextEdit, QScrollArea)
from PyQt5.QtCore import Qt, QPoint
from entities.component import Component
from utils.constants import OBJECT_COLORS, TID, PACKET
from gui.g2h_widget import G2hWidget
from gui.h2g_widget import H2gWidget
from gui.log_colors_dialog import LogColorDialog
from gui.packets_colors import get_colors_by_tids
from entities.host_interface import HostInterface


class HostInterfaceWidget(QWidget):
    def __init__(self, host_interface: HostInterface, parent: Optional[QWidget] = None) -> None:
        # Initialize the HostInterfaceWidget with HostInterface instance and optional parent widget.
        super().__init__(parent)
        self.host_interface = host_interface
        self.host_interface_tids = self.host_interface.get_attribute_from_active_logs(TID)
        self.colors = list(get_colors_by_tids(self.host_interface_tids))  # Convert set to list
        self.colors_bmt = list(self.get_colors(self.host_interface.bmt))  # Convert set to list
        self.colors_H2G = list(self.get_colors(self.host_interface.h2g))  # Convert set to list
        self.colors_G2H = list(self.get_colors(self.host_interface.g2h))  # Convert set to list
        self.colors_pcie = list(self.get_colors(self.host_interface.pcie))  # Convert set to list
        self.packet_messages = self.host_interface.get_attribute_from_active_logs(PACKET)  # Fetch packet messages

        self.color_map = self.create_color_map()  # Create a color map for TIDs
        self.setContextMenuPolicy(Qt.CustomContextMenu)  # Enable custom context menu
        self.customContextMenuRequested.connect(self.show_host_interface_logs)
        self.initUI()

    def initUI(self) -> None:
        # Initialize the user interface for the HostInterfaceWidget.
        self.main_layout = QVBoxLayout()

        self.outer_frame = QFrame()
        self.outer_frame.setFrameShape(QFrame.StyledPanel)
        self.outer_frame.setFrameShadow(QFrame.Raised)

        # Ensure colors lists are not empty before accessing their elements
        self.title_color = self.colors[0] if self.colors else 'white'
        self.title_color_bmt = self.colors_bmt[0] if self.colors_bmt else 'white'
        self.title_color_H2G = self.colors_H2G[0] if self.colors_H2G else 'white'
        self.title_color_G2H = self.colors_G2H[0] if self.colors_G2H else 'white'
        self.title_color_pcie = self.colors_pcie[0] if self.colors_pcie else 'white'

        self.title_label = QLabel("<b>HostInterface</b>")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet(
            f'border-bottom: 2px solid black; padding-bottom: 5px; margin-bottom: 10px; background-color: {self.title_color};')

        self.frame_layout = QVBoxLayout()
        self.frame_layout.addWidget(self.title_label)

        self.toggle_button = QPushButton("Show Details", self)
        self.toggle_button.clicked.connect(self.toggle_content)
        self.frame_layout.addWidget(self.toggle_button)

        # Layout for component buttons
        self.component_buttons_layout = QWidget()  # Changed to QWidget for visibility toggling
        self.component_buttons_layout.setLayout(QHBoxLayout())
        self.create_component_button(self.host_interface.bmt)
        self.create_component_button(self.host_interface.h2g, clickable=True)
        self.create_component_button(self.host_interface.g2h, clickable=True)
        self.create_component_button(self.host_interface.pcie)
        self.component_buttons_layout.setVisible(False)  # Initially hidden
        self.frame_layout.addWidget(self.component_buttons_layout)

        self.outer_frame.setLayout(self.frame_layout)
        self.main_layout.addWidget(self.outer_frame)
        self.setLayout(self.main_layout)

        self.h2g_widget = H2gWidget(self.host_interface.h2g) if self.host_interface.h2g else None
        self.g2h_widget = G2hWidget(self.host_interface.g2h) if self.host_interface.g2h else None

        self.details_widget = QWidget()
        self.details_layout = QVBoxLayout()
        self.details_widget.setLayout(self.details_layout)
        self.details_widget.setVisible(False)
        self.main_layout.addWidget(self.details_widget)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def toggle_content(self) -> None:
        # Toggle the visibility of component buttons and details widget.
        is_visible = self.component_buttons_layout.isVisible()
        self.component_buttons_layout.setVisible(not is_visible)
        self.details_widget.setVisible(False)
        self.toggle_button.setText("Hide Details" if not is_visible else "Show Details")

    def create_color_map(self) -> Dict[str, str]:
        # Create a mapping of TID to colors.
        color_map = {}
        for idx, tid in enumerate(self.host_interface_tids):
            if idx < len(self.colors):
                color_map[tid] = self.colors[idx]
            else:
                color_map[tid] = 'white'  # Default color if no color is available
        return color_map

    def create_component_button(self, component: Component, clickable: Optional[bool] = False) -> None:
        # Create a button for the given component and add it to the layout.
        if component is None:
            return

        button = QPushButton(component.type_name, self)
        button.setFixedSize(200, 70)
        color = OBJECT_COLORS.get(component.type_name, 'white')
        background_color = 'white'

        # Set the background color based on the component type
        if component.type_name == 'bmt':
            background_color = self.title_color_bmt
        elif component.type_name == 'H2G':
            background_color = self.title_color_H2G
        elif component.type_name == 'G2H':
            background_color = self.title_color_G2H
        elif component.type_name == 'pcie':
            background_color = self.title_color_pcie

        button.setStyleSheet(
            f'background-color: {background_color}; border: 2.5px solid {color}; border-radius: 7px; padding: 10px; margin: 10px;')

        # Set cursor style: hand pointer for H2G and G2H, forbidden cursor for others
        if component.type_name in ['H2G', 'G2H']:
            button.setCursor(Qt.PointingHandCursor)
        else:
            button.setCursor(Qt.ForbiddenCursor)

        # If the button is clickable, connect it to show details for the component
        if clickable:
            button.clicked.connect(lambda: self.show_details(component.type_name))

        # Connect right-click to show colors and logs
        button.setContextMenuPolicy(Qt.CustomContextMenu)
        button.customContextMenuRequested.connect(
            lambda point: self.show_colors_and_logs(component, f"{component.type_name} Logs"))

        self.component_buttons_layout.layout().addWidget(button)

    def show_details(self, section_name: str) -> None:
        # Show details for the selected section (H2G or G2H).
        self.details_widget.setVisible(True)
        if section_name == 'H2G' and self.h2g_widget:
            self.g2h_widget.hide_components()
            self.details_layout.addWidget(self.h2g_widget)
            self.h2g_widget.show_components()
            self.h2g_widget.setCursor(Qt.PointingHandCursor)

        elif section_name == 'G2H' and self.g2h_widget:
            self.h2g_widget.hide_components()
            self.details_layout.addWidget(self.g2h_widget)
            self.g2h_widget.show_components()
            self.g2h_widget.setCursor(Qt.PointingHandCursor)

        else:
            print(f"Details for {section_name} not found or not available.")

    def show_context_menu_for_component(self, point: QPoint, component: Component) -> None:
        # Show a context menu for the given component.
        context_menu = QMenu(self)
        log_action = QAction(f"Show {component.type_name} Logs", self)
        log_action.triggered.connect(lambda: self.show_colors_and_logs(component, f"{component.type_name} Logs"))
        context_menu.addAction(log_action)
        context_menu.exec_(self.mapToGlobal(point))

    def show_context_menu(self, point: QPoint) -> None:
        # Show a general context menu.
        context_menu = QMenu(self)
        context_menu.exec_(self.mapToGlobal(point))

    def show_colors_and_logs(self, component: Component, title: str) -> None:
        # Show a dialog with colors and logs for the given component.
        try:
            dialog = LogColorDialog(component, title, self)
            dialog.exec_()
        except Exception as e:
            print(f"An error occurred: {e}")

    def show_host_interface_logs(self, point: QPoint) -> None:
        # Show a dialog with logs for the entire HostInterface.
        try:
            dialog = LogColorDialog(self.host_interface, "HostInterface Logs", self)
            dialog.exec_()
        except Exception as e:
            print(f"An error occurred: {e}")

    def get_colors(self, data) -> list:
        # Fetch colors for the given data.
        data_tids = data.get_attribute_from_active_logs(TID)
        return list(get_colors_by_tids(data_tids))
