from typing import Optional

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QMouseEvent
from utils.constants import TID, PACKET
from entities.cluster import Cluster
from gui.log_colors_dialog import LogColorDialog
from gui.packets_colors import get_colors_by_tids


class ClusterWidget(QWidget):
    def __init__(self, cluster: Cluster, parent: Optional[QWidget] = None) -> None:
        # Initialize with a cluster and optional parent widget
        super().__init__(parent)
        self.cluster = cluster
        self.cluster_tids = self.cluster.get_attribute_from_active_logs(TID)
        self.colors = list(get_colors_by_tids(self.cluster_tids))  # Convert set to list
        self.packet_messages = self.cluster.get_attribute_from_active_logs(PACKET)  # Fetch packet messages
        self.initUI()

    def initUI(self) -> None:
        # Set up the user interface
        layout = QVBoxLayout()
        layout.setSpacing(0)  # Reduce spacing between widgets
        layout.setContentsMargins(0, 0, 0, 0)  # No margins
        self.setLayout(layout)

        color = QColor(self.cluster.color)
        text_color = color.name()
        self.label = QLabel(f'{self.cluster.type_name}\nCluster {self.cluster.id}', self)
        self.label.setAlignment(Qt.AlignCenter)
        text_color = text_color if self.cluster.is_enable else "lightgrey"
        self.label.setStyleSheet(f'color: {text_color}; font-size: 12px; padding: 0px;')

        layout.addWidget(self.label)

        back_color = "lightgrey"
        if self.colors:
            back_color = self.colors[0]

        self.setStyleSheet(f'background-color: {back_color}; border: 2px dashed {text_color};')

        self.setCursor(Qt.PointingHandCursor)
        self.setEnabled(self.cluster.is_enable)
        self.mousePressEvent = self.show_log_messages  # Show log messages on right click

    def show_log_messages(self, event: QMouseEvent) -> None:
        # Show log messages or cluster info based on the event button
        if event.button() == Qt.RightButton:
            dialog = LogColorDialog(self.cluster, "Cluster Logs", self)
            dialog.exec_()
        else:
            self.show_cluster_info(event)

    def show_cluster_info(self, event: QMouseEvent) -> None:
        # Show cluster info in the parent widget
        from gui.quad_widget import QuadWidget  # Import to avoid circular dependency
        parent_widget = self.parent()
        while parent_widget and not isinstance(parent_widget, QuadWidget):
            parent_widget = parent_widget.parent()
        if parent_widget:
            parent_widget.show_cluster_info(self.cluster)

    def update_display(self) -> None:
        # Update display with new colors and packet messages
        self.colors = list(get_colors_by_tids(self.cluster.get_attribute_from_active_logs(TID)))
        self.packet_messages = self.get_messages_by_packet()  # Update packet messages
        back_color = self.colors[0] if self.colors else "lightgrey"
        self.setStyleSheet(f'background-color: {back_color}; border: 2px dashed {self.cluster.color};')
        self.label.setText(f'{self.cluster.type_name}\nCluster {self.cluster.id}')
