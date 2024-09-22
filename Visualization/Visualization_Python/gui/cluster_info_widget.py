from PyQt5.QtGui import QCloseEvent, QContextMenuEvent
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QHBoxLayout,
                             QGridLayout, QScrollArea, QLayout)
from PyQt5.QtCore import Qt
from typing import Optional
from entities.cluster import Cluster
from entities.component import Component
from gui.component_widget import ComponentWidget
from gui.log_colors_dialog import LogColorDialog
from gui.mcu_widget import McuInfoWidget
from entities.mcu import Mcu
from gui.packets_colors import get_colors_by_tids
from utils.constants import TID, OBJECT_COLORS


class ClusterInfoWidget(QWidget):

    def __init__(self, cluster: Cluster, parent: Optional[QWidget] = None) -> None:
        # Initialize with a cluster and optional parent widget
        super().__init__(parent)
        self.cluster = cluster
        self.initUI()

    def initUI(self) -> None:
        # Set up the user interface
        self.setStyleSheet(
            f'background-color: #f0f0f0; border: 1px solid {self.cluster.color}; padding: 0px; border-radius: 10px;')
        layout = QVBoxLayout()

        # Header Layout
        header_layout = QHBoxLayout()
        close_button = QPushButton("X")
        close_button.clicked.connect(self.close)
        close_button.setObjectName("back_red")
        close_button.setStyleSheet(
            "background-color: red; color: white; font-weight: bold; border: none; padding: 10px;")
        close_button.setCursor(Qt.PointingHandCursor)
        header_layout.addWidget(close_button, alignment=Qt.AlignRight)
        layout.addLayout(header_layout)

        # Scroll Area for Grid Layout
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("border: none;")

        scroll_area_widget = QWidget()
        scroll_area_layout = QGridLayout(scroll_area_widget)
        scroll_area_layout.setSpacing(5)

        components = self.cluster.get_details()
        for i, component in enumerate(components):
            component_widget = ComponentWidget(component, component.type_name)
            component_tids = component.get_attribute_from_active_logs(TID)
            colors = list(get_colors_by_tids(component_tids))
            back_color = colors[0] if colors else "lightgrey"
            color = OBJECT_COLORS.get(component_widget.type_name, 'white')
            component_widget.setStyleSheet(
                f'background-color: {back_color}; border: 1px solid {color}; padding: 0px; border-radius: 5px;')
            component_widget.setMinimumSize(100, 100)  # Set minimum size for each component

            # Set cursor based on component type
            if component.type_name == "MCU":
                component_widget.setCursor(Qt.PointingHandCursor)  # Set cursor to Pointer for MCU
                component_widget.mousePressEvent = lambda event, comp=component: self.handle_mouse_event(event, comp)
            else:
                component_widget.setCursor(Qt.ForbiddenCursor)  # Set cursor to Forbidden for non-MCU

            # Directly call show_logs on right-click
            component_widget.contextMenuEvent = lambda event, comp=component: self.show_logs(comp)

            row = i // 4
            col = i % 4
            scroll_area_layout.addWidget(component_widget, row, col)
            scroll_area_widget.setObjectName("scroll_area_widget")
        scroll_area.setWidget(scroll_area_widget)
        scroll_area.setObjectName("scroll_area")
        layout.addWidget(scroll_area)

        self.setLayout(layout)
        self.setWindowTitle(f"Cluster ID: {self.cluster.id}")

    def handle_mouse_event(self, event: QContextMenuEvent, component: Component) -> None:
        # Handle mouse events for components
        if event.button() == Qt.LeftButton and component.type_name == "MCU":
            self.show_mcu_info(component)

    def show_mcu_info(self, mcu: Mcu) -> None:
        # Display MCU information
        self.previous_layout = self.layout()
        self.mcu_info_widget = McuInfoWidget(mcu, self)
        self.build_m(mcu)

    def show_again(self) -> None:
        # Show previously hidden widgets
        self.layout().addWidget(self.widget_to_remove2, alignment=Qt.AlignRight)
        self.layout().addWidget(self.widget_to_remove)
        self.widget_to_remove2.show()
        self.widget_to_remove.show()

    def build_m(self, mcu: Mcu) -> None:
        # Build MCU info widget and hide unnecessary widgets
        self.mcu_info_widget = McuInfoWidget(mcu, self)
        self.mcu_info_widget.setObjectName("mcu")
        self.layout().addWidget(self.mcu_info_widget)

        self.widget_to_remove = self.findChild(QWidget, name="scroll_area")
        self.widget_to_remove2 = self.findChild(QWidget, name="back_red")
        self.widget_to_remove.hide()  # Hide the widget
        self.widget_to_remove2.hide()  # Hide the widget

    def clear_layout(self, layout: Optional[QLayout] = None) -> None:
        # Recursively clear layout contents
        if layout is None:
            layout = self.layout()

        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                pass
            elif item.layout():
                self.clear_layout(item.layout())  # Continue clearing nested layouts if present

    def show_logs(self, component) -> None:
        # Show logs for the selected component
        if component:
            dialog = LogColorDialog(component, "Logs and Colors", self)
            dialog.exec_()

    def closeEvent(self, event: QCloseEvent) -> None:
        # Handle close event for the widget
        from gui.quad_widget import QuadWidget
        if isinstance(self.parent(), QuadWidget):
            self.parent().show_quad(1)
        else:
            super().closeEvent(event)
