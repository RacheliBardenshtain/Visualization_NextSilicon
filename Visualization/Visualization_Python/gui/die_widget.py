from PyQt5.QtGui import QResizeEvent
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QMainWindow
from PyQt5.QtCore import Qt
from entities.die import Die
from gui.quad_widget import QuadWidget
from utils.data_manager import DataManager
from typing import Dict, Optional


class DieWidget(QWidget):
    def __init__(self, data_manager: DataManager, dies: Dict[str, Die], main_window: QMainWindow) -> None:
        # Initialize with DataManager, dies dictionary, and main window
        super().__init__()
        self.data_manager = data_manager
        self.main_window = main_window
        self.dies = dies
        self.initUI()

    def initUI(self) -> None:
        # Initialize UI elements
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Container for Quad Matrix
        self.quad_container = QWidget()
        self.quad_layout = QGridLayout(self.quad_container)
        self.quad_layout.setSpacing(0)  # Reduced spacing
        self.quad_layout.setContentsMargins(140, 0, 140, 0)  # Add small margins
        self.layout.addWidget(self.quad_container)

        # Initially hide the quad_container
        self.quad_container.setVisible(False)

    def show_quads(self, die_index: int) -> None:
        # Display the quads for a given die index
        try:
            die = self.dies.get(die_index)
            if die is None:
                print("Error: die is None")
                return

            # Clear previous widgets from the quad layout
            self.clear_layout(self.quad_layout)

            # Display new matrix of 4 quads
            for i in range(2):
                for j in range(2):
                    quad = die.quads[i][j]
                    if quad:
                        quad_widget = QuadWidget(quad, j == 1, self)  # Pass position (i, j)
                        if quad.is_enable:
                            quad_widget.setCursor(Qt.PointingHandCursor)
                        else:
                            quad_widget.setCursor(Qt.ForbiddenCursor)
                    else:
                        quad_widget = QLabel('Empty', self)
                        quad_widget.setAlignment(Qt.AlignCenter)
                        quad_widget.setStyleSheet(
                            'border: 1px dashed black; min-width: 150px; min-height: 150px; background-color: red;')
                    self.quad_layout.addWidget(quad_widget, i, j, alignment=Qt.AlignCenter)

            self.adjust_quad_sizes()
            self.quad_container.setVisible(True)
        except Exception as e:
            print(f"Error showing quads: {e}")

    def clear_layout(self, layout: Optional[QGridLayout] = None) -> None:
        # Clear previous widgets from the layout
        if layout is None:
            layout = self.quad_layout

        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.clear_layout(item.layout())
        layout.update()

    def adjust_quad_sizes(self) -> None:
        # Adjust the sizes of the quads
        try:
            size = self.size().width() // 3 + 150
            for i in range(2):
                for j in range(2):
                    item = self.quad_layout.itemAtPosition(i, j)
                    if item:
                        widget = item.widget()
                        if widget:
                            widget.setFixedSize(size, size)
        except Exception as e:
            print(f"Error adjusting quad sizes: {e}")

    def resizeEvent(self, event: QResizeEvent) -> None:
        # Handle resize event
        self.adjust_quad_sizes()
        super().resizeEvent(event)
