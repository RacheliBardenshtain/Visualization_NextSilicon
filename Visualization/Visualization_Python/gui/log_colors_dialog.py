from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect, QTimer
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QWidget, QTextEdit, QScrollArea, QLabel, QGridLayout, QPushButton
)
from PyQt5.QtGui import QFont
from gui.packets_colors import get_colors_by_tids
from utils.constants import TID, PACKET
from typing import List

class LogColorDialog(QDialog):
    def __init__(self, data, title: str, parent=None) -> None:
        super().__init__(parent)
        self.data = data
        self.title = title
        self.initUI()

    def initUI(self) -> None:
        # Retrieve TIDs and packets from logs
        tids = self.data.get_attribute_from_active_logs(TID)
        packets = self.data.get_attribute_from_active_logs(PACKET)
        colors = list(get_colors_by_tids(tids))

        # Create a map between colors and TIDs
        color_tid_map = {color: set() for color in colors}
        for tid, color in zip(tids, colors):
            color_tid_map[color].add(tid)

        self.setWindowTitle(self.title)
        dialog_layout = QVBoxLayout(self)

        # If there are no packets, show a message
        if not packets:
            no_logs_label = QLabel("No logs available")
            no_logs_label.setAlignment(Qt.AlignCenter)
            no_logs_label.setFont(QFont("Arial", 12))
            dialog_layout.addWidget(no_logs_label)
        else:
            # Create header to display TID-to-color mapping
            header_widget = QWidget()
            header_layout = QGridLayout(header_widget)
            row, col = 0, 0
            max_columns = 4

            # Create buttons for each TID with corresponding color
            for color, tids in color_tid_map.items():
                tids_text = (str(tids))
                color_button = QPushButton(f" Thread Id: {tids_text} ")

                # Style the button with appropriate background color
                color_button.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {color}; 
                        color: black; 
                        padding: 10px 10px; 
                        margin: 5px; 
                        border-radius: 10px; 
                        font-size: 14px;
                    }}
                    QPushButton:hover {{
                        background-color: #d3d3d3;
                        color: black;
                    }}
                """)

                # Connect button to the filtering function for specific TIDs
                color_button.clicked.connect(self.create_tid_filter_function(tids))
                color_button.setCursor(Qt.PointingHandCursor)
                header_layout.addWidget(color_button, row, col)
                col += 1
                if col >= max_columns:
                    col = 0
                    row += 1

            # Wrap header widget with scroll area for TIDs
            header_scroll_area = QScrollArea()
            header_scroll_area.setWidgetResizable(True)
            header_scroll_area.setWidget(header_widget)
            header_scroll_area.setFixedHeight(150)  # Limit the height of the TID area
            header_scroll_area.setStyleSheet("background-color: white; border: none;")

            header_widget.setStyleSheet(
                "background-color: white; padding: 10px; border-bottom: 1px solid lightgray;")
            dialog_layout.addWidget(header_scroll_area)

            # Create content area to display logs
            self.content_widget = QWidget()
            self.content_layout = QVBoxLayout(self.content_widget)
            self.update_content(packets, colors)

            # Add scroll area for content
            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)
            scroll_area.setWidget(self.content_widget)
            scroll_area.setStyleSheet("background-color: transparent; border: none;")
            dialog_layout.addWidget(scroll_area)

            # Button to show all logs
            self.show_all_button = QPushButton("Show All Logs")
            self.show_all_button.setCursor(Qt.PointingHandCursor)
            self.show_all_button.clicked.connect(self.show_all_logs)
            self.show_all_button.setStyleSheet("""
                QPushButton {
                    background-color: linen; 
                    color: black; 
                    font-size: 14px; 
                    border-radius: 10px; 
                    border: 2px solid black;
                    margin-top: 10px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
            """)
            dialog_layout.addWidget(self.show_all_button)

        # Set dialog size and style
        self.setFixedWidth(800)
        self.setLayout(dialog_layout)
        self.setStyleSheet("""
            background-color: white;
        """)

    def create_tid_filter_function(self, tids: set) -> callable:
        """ Create a function that filters the logs by the given TIDs """
        def filter_function(event) -> None:
            packets = self.data.get_attribute_from_active_logs(PACKET)
            colors = list(get_colors_by_tids(self.data.get_attribute_from_active_logs(TID)))
            filtered_packets = [pkt for i, pkt in enumerate(packets) if self.data.get_attribute_from_active_logs(TID)[i] in tids]
            filtered_colors = [colors[i] for i in range(len(packets)) if self.data.get_attribute_from_active_logs(TID)[i] in tids]
            self.update_content(filtered_packets, filtered_colors)
        return filter_function

    def show_all_logs(self) -> None:
        """ Show all logs in the content area """
        tids = self.data.get_attribute_from_active_logs(TID)
        packets = self.data.get_attribute_from_active_logs(PACKET)
        colors = list(get_colors_by_tids(tids))
        self.update_content(packets, colors)

    def update_content(self, packets: List[str], colors: List[str]) -> None:
        """ Update the content area with the logs """
        # Clear current content
        while self.content_layout.count():
            child = self.content_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Add new content without gaps
        for i, packet in enumerate(packets):
            color = colors[i] if i < len(colors) else "none"
            text_edit = QTextEdit()
            text_edit.setPlainText(f"Packet: {packet}")
            text_edit.setReadOnly(True)
            if color != "none":
                text_edit.setStyleSheet(f"background-color: {color}; border: none;")
            else:
                text_edit.setStyleSheet("border: solid 1px black;")
            self.content_layout.addWidget(text_edit)

        self.content_layout.addStretch()  # Ensure content fills and scrolls properly
