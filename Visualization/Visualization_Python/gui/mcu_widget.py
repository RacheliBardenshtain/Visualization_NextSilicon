from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QGridLayout
from utils.constants import OBJECT_COLORS
from entities.mcu import Mcu
from typing import Optional


class McuInfoWidget(QWidget):
    mcu_closed = pyqtSignal()  # Signal to indicate that MCU is closed

    def __init__(self, mcu: Mcu, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.mcu = mcu
        self.initUI()

    def initUI(self) -> None:
        # Set the stylesheet for the widget
        self.setStyleSheet(
            f'background-color: lightgrey; border: 10px solid {OBJECT_COLORS["MCU"]}; '
            'padding: 0px; border-radius: 20px;'
        )

        # Create main layout and header layout
        layout = QVBoxLayout()
        header_layout = QHBoxLayout()

        # Create and configure close button
        close_button = QPushButton("X")
        close_button.clicked.connect(self.back)
        close_button.setCursor(Qt.PointingHandCursor)
        close_button.setStyleSheet(
            "background-color: red; color: white; font-weight: bold; "
            "border: solid; border-radius: 6px; padding: 10px;"
        )
        header_layout.addWidget(close_button, alignment=Qt.AlignRight)

        # Add header layout to main layout
        layout.addLayout(header_layout)

        # Create grid layout for MCU components
        grid_layout = QGridLayout()
        grid_layout.setSpacing(5)

        # Add components to the grid layout
        mcu_components = self.mcu.get_details()
        for i, component in enumerate(mcu_components):
            from gui.cluster_info_widget import ComponentWidget

            # Create and add component widgets to the grid
            component_widget = ComponentWidget(component, component.type_name)
            row = i // 4
            col = i % 4
            grid_layout.addWidget(component_widget, row, col)

        # Add grid layout to main layout
        layout.addLayout(grid_layout)

        # Set the main layout and window title
        self.setLayout(layout)
        self.setWindowTitle(f"MCU Details: {self.mcu.id}")

    def back(self):
        # Close the widget and signal that MCU is closed
        self.close()
        self.mcu_closed.emit()  # Emit signal to notify that MCU is closed
        self.parent().show_again()  # Call parent's method to show the previous widget again
