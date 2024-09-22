from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QGridLayout, QMenu, QAction, QDialog, QTextEdit, \
    QScrollArea
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QMouseEvent
from entities.cluster import Cluster
from utils.constants import TID, PACKET
from gui.cluster_info_widget import ClusterInfoWidget
from gui.cluster_widget import ClusterWidget
from gui.log_colors_dialog import LogColorDialog
from gui.packets_colors import get_colors_by_tids
from entities.quad import Quad
from typing import Optional


class QuadWidget(QWidget):
    def __init__(self, quad: Quad, is_right_side: bool, parent: Optional[QWidget] = None):
        # Initializes the QuadWidget class
        super().__init__(parent)
        self.quad = quad
        self.quad_tids = self.quad.get_attribute_from_active_logs(TID)
        self.hbm_tids = self.quad.hbm.get_attribute_from_active_logs(TID)
        self.colors = list(get_colors_by_tids(self.quad_tids))
        self.hbm_colors = list(get_colors_by_tids(self.hbm_tids))
        self.packet_messages = self.quad.get_attribute_from_active_logs(PACKET)
        self.hbm_packet_messages = self.quad.hbm.get_attribute_from_active_logs(PACKET)
        self.is_right_side = is_right_side
        self.parent = parent
        self.initUI()

    def initUI(self) -> None:
        # Sets up the initial UI components
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.grid_layout = QGridLayout()
        self.layout.addLayout(self.grid_layout)

        self.label_quad = QLabel(self.quad.name, self)
        self.label_quad.setAlignment(Qt.AlignCenter)
        if self.is_right_side:
            self.grid_layout.addWidget(self.label_quad, 0, 0)
        else:
            self.grid_layout.addWidget(self.label_quad, 0, 1)

        self.add_hbm()

        if self.is_right_side:
            self.grid_layout.setColumnStretch(0, 4)
        else:
            self.grid_layout.setColumnStretch(1, 4)

        back_color = 'lightgrey'
        if self.colors:
            back_color = self.colors[0]

        self.setStyleSheet(f'background-color: {back_color}; border: 2px dashed black;')
        color = "green" if self.quad.is_enable else "lightgrey"
        self.setStyleSheet(f'background-color: {back_color}; border: 2px dashed {color};')
        self.setEnabled(self.quad.is_enable)

    def add_hbm(self) -> None:
        # Adds HBM label to the layout
        self.label_hbm = QLabel(self.quad.hbm.type_name + "\n" + self.quad.name[:2], self)
        self.label_hbm.setAlignment(Qt.AlignCenter)
        hbm_back_color = "grey"
        if self.hbm_colors:
            hbm_back_color = self.hbm_colors[0]

        self.label_hbm.setStyleSheet(f"background-color: {hbm_back_color};")
        if self.is_right_side:
            self.grid_layout.addWidget(self.label_hbm, 0, 1)
        else:
            self.grid_layout.addWidget(self.label_hbm, 0, 0)

        self.label_hbm.mousePressEvent = self.hbm_mouse_press_event

    def hbm_mouse_press_event(self, event: QMouseEvent) -> None:
        # Handles mouse press events on the HBM label
        if event.button() == Qt.RightButton:
            self.show_hbm_log_messages()  # Directly show logs

    def mousePressEvent(self, event: QMouseEvent) -> None:
        # Handles mouse press events
        try:
            if event.button() == Qt.RightButton:
                self.show_log_messages()  # Directly show logs
            elif not self.is_hbm(event.pos()):
                self.show_clusters()
        except Exception as e:
            print(f"Error handling mouse press event: {e}")

    def show_hbm_context_menu(self, event: QMouseEvent) -> None:
        # Shows context menu for HBM label
        context_menu = QMenu(self)

        show_log_action = QAction("Show HBM Log Messages", self)
        show_log_action.triggered.connect(self.show_hbm_log_messages)
        context_menu.addAction(show_log_action)

        context_menu.exec_(self.mapToGlobal(event.pos()))

    def show_hbm_log_messages(self) -> None:
        # Shows HBM log messages in a dialog
        try:
            dialog = LogColorDialog(self.quad.hbm, "HBM Log Messages", self)
            dialog.exec_()
        except Exception as e:
            print(f"Error showing HBM log messages: {e}")

    def is_hbm(self, pos: QPoint) -> bool:
        # Checks if the position is within the HBM label
        try:
            return self.label_hbm.geometry().contains(pos)
        except Exception as e:
            print(f"Error checking HBM: {e}")
            return False

    def show_context_menu(self, event: QMouseEvent) -> None:
        # Shows context menu for the quad
        try:
            context_menu = QMenu(self)
            show_log_action = QAction("Show Log Messages", self)
            show_log_action.triggered.connect(self.show_log_messages)
            context_menu.addAction(show_log_action)

            context_menu.exec_(self.mapToGlobal(event.pos()))
        except Exception as e:
            print(f"Error showing context menu: {e}")

    def show_log_messages(self) -> None:
        # Shows quad log messages in a dialog
        try:
            dialog = LogColorDialog(self.quad, "Quad Log Messages", self)
            dialog.exec_()
        except Exception as e:
            print(f"Error showing log messages: {e}")

    def show_clusters(self, event=None) -> None:
        # Displays cluster widgets
        try:
            self.setCursor(Qt.ForbiddenCursor)

            if self.label_quad:
                self.label_quad.hide()

            if hasattr(self, 'cluster_layout'):
                while self.cluster_layout.count():
                    item = self.cluster_layout.takeAt(0)
                    widget = item.widget()
                    if widget:
                        widget.deleteLater()

            self.cluster_layout = QGridLayout()
            self.cluster_layout.setSpacing(0)
            if self.is_right_side:
                self.grid_layout.addLayout(self.cluster_layout, 0, 0, 1, 1)
            else:
                self.grid_layout.addLayout(self.cluster_layout, 0, 1, 1, 1)

            for row in self.quad.clusters:
                for cluster in row:
                    if cluster is not None:
                        cluster_widget = ClusterWidget(cluster, self)
                        self.cluster_layout.addWidget(cluster_widget, cluster.row, cluster.col)

            back_button = QPushButton("Back To " + self.quad.name)
            back_button.setCursor(Qt.PointingHandCursor)
            back_button.setStyleSheet('background-color : lightgrey')
            back_button.clicked.connect(self.show_previous_state)
            self.cluster_layout.addWidget(back_button, len(self.quad.clusters), 0, 1, len(self.quad.clusters[0]))

            self.setCursor(Qt.ArrowCursor)
        except Exception as e:
            print(f"Error showing clusters: {e}")

    def show_previous_state(self) -> None:
        # Shows the previous state of the widget
        try:
            if self.label_quad:
                self.label_quad.show()
            if hasattr(self, 'cluster_layout'):
                while self.cluster_layout.count():
                    item = self.cluster_layout.takeAt(0)
                    widget = item.widget()
                    if widget:
                        widget.deleteLater()
                self.grid_layout.removeItem(self.cluster_layout)
                del self.cluster_layout
        except Exception as e:
            print(f"Error showing previous state: {e}")

    def show_quad_info(self) -> None:
        # Displays information about the quad
        try:
            cluster_info_widget = ClusterInfoWidget(self.quad)
            cluster_info_widget.show()
        except Exception as e:
            print(f"Error showing quad info: {e}")

    def show_cluster_info(self, cluster: Cluster) -> None:
        # Displays information about the cluster
        self.clear_layout()
        cluster_info_widget = ClusterInfoWidget(cluster, self)
        self.layout.addWidget(cluster_info_widget)

    def show_quad(self, init: Optional[bool] = 0) -> None:
        # Updates and shows the quad widget
        if self.quad.is_enable:
            self.setCursor(Qt.PointingHandCursor)
        else:
            self.setCursor(Qt.ForbiddenCursor)
        self.setStyleSheet('border: 2px dashed black;')
        back_color = 'lightgrey'
        if self.colors:
            back_color = self.colors[0]
        color = "green" if self.quad.is_enable else "lightgrey"
        self.setStyleSheet(f'background-color:{back_color}; border: 2px dashed {color};')

        self.clear_layout()

        self.grid_layout = QGridLayout()
        self.layout.addLayout(self.grid_layout)

        self.label_quad = QLabel(self.quad.name, self)
        self.label_quad.setAlignment(Qt.AlignCenter)
        if self.is_right_side:
            self.grid_layout.addWidget(self.label_quad, 0, 0)
        else:
            self.grid_layout.addWidget(self.label_quad, 0, 1)
        self.add_hbm()

        if self.is_right_side:
            self.grid_layout.setColumnStretch(0, 4)
        else:
            self.grid_layout.setColumnStretch(1, 4)

        self.adjustSize()
        if init:
            self.show_clusters()

    def clear_layout(self, layout: Optional[QGridLayout] = None) -> None:
        # Clears the specified layout
        if layout is None:
            layout = self.layout

        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
            elif item.layout():
                self.clear_layout(item.layout())

        layout.update()