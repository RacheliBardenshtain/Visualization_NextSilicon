from PyQt5.QtCore import Qt, QTime, pyqtSignal
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QSlider, QToolTip
from PyQt5.QtGui import QMouseEvent, QPainter, QColor, QPen
import datetime

class RangeSlider(QSlider):
    range_changed = pyqtSignal(int, int)

    def __init__(self, orientation: Qt.Orientation, main_window: QWidget = None) -> None:
        super().__init__(orientation, main_window)
        self.start_handle_pos = 0
        self.end_handle_pos = self.maximum()
        self.setMouseTracking(True)
        self.setStyleSheet("QSlider::handle:horizontal { width: 0px; }")

    def mousePressEvent(self, event: QMouseEvent) -> None:
        pos = self.valueFromPosition(event.pos())
        if abs(pos - self.start_handle_pos) < abs(pos - self.end_handle_pos):
            self.start_handle_pos = pos
        else:
            self.end_handle_pos = pos
        self.range_changed.emit(self.start_handle_pos, self.end_handle_pos)
        self.update()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if event.buttons() & Qt.LeftButton:
            pos = self.valueFromPosition(event.pos())
            if abs(pos - self.start_handle_pos) < abs(pos - self.end_handle_pos):
                self.start_handle_pos = pos
            else:
                self.end_handle_pos = pos
            self.range_changed.emit(self.start_handle_pos, self.end_handle_pos)
            self.update()
        self.updateToolTip(event)

    def updateToolTip(self, event: QMouseEvent) -> None:
        pos = self.valueFromPosition(event.pos())
        time = self.start_time + datetime.timedelta(seconds=pos)
        formatted_time = time.strftime("%H:%M:%S")
        QToolTip.showText(event.globalPos(), formatted_time)

    def valueFromPosition(self, pos: QMouseEvent) -> int:
        return round(self.minimum() + (self.maximum() - self.minimum()) * pos.x() / self.width())

    def positionFromValue(self, value: int) -> int:
        return round(self.width() * (value - self.minimum()) / (self.maximum() - self.minimum()))

    def paintEvent(self, event) -> None:
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setPen(QPen(QColor(0, 0, 255), 2))
        painter.setBrush(QColor(0, 0, 255))
        start_pos = self.positionFromValue(self.start_handle_pos)
        painter.drawEllipse(start_pos - 5, self.height() // 2 - 5, 15, 15)
        painter.setPen(QPen(QColor(255, 0, 0), 2))
        painter.setBrush(QColor(255, 0, 0))
        end_pos = self.positionFromValue(self.end_handle_pos)
        painter.drawEllipse(end_pos - 5, self.height() // 2 - 5, 15, 15)

class TimelineWidget(QWidget):
    def __init__(self, data_manager, start_time=None, end_time=None, main_window=None) -> None:
        super().__init__(main_window)
        self.data_manager = data_manager
        self.start_time = start_time
        self.end_time = end_time
        self.main_window = main_window
        self.previous_start_pos = 0
        self.previous_end_pos = None  # Initialize to None for comparison
        self.initUI()
        self.setupTimes()

        # Connect the range_changed signal to update_labels
        self.timeline_slider.range_changed.connect(self.update_labels)

    def initUI(self) -> None:
        self.layout = QHBoxLayout(self)
        self.setLayout(self.layout)

        self.start_label = QLabel(self)
        self.layout.addWidget(self.start_label)

        self.timeline_slider = RangeSlider(Qt.Horizontal, self)
        self.layout.addWidget(self.timeline_slider)

        self.end_label = QLabel(self)
        self.layout.addWidget(self.end_label)

    def setupTimes(self) -> None:
        if self.start_time is None or self.end_time is None:
            now = datetime.datetime.now()
            self.start_time = now
            self.end_time = now + datetime.timedelta(minutes=30)

        self.timeline_slider.start_time = self.start_time

        start_time_q = QTime(self.start_time.hour, self.start_time.minute, self.start_time.second)
        end_time_q = QTime(self.end_time.hour, self.end_time.minute, self.end_time.second)

        self.set_start_time(start_time_q.toString("HH:mm:ss"))
        self.set_end_time(end_time_q.toString("HH:mm:ss"))

        seconds_range = int((self.end_time - self.start_time).total_seconds())
        self.timeline_slider.setRange(0, seconds_range)
        self.timeline_slider.start_handle_pos = 0
        self.timeline_slider.end_handle_pos = seconds_range

    def update_labels(self, start_pos: int, end_pos: int) -> None:
        start_time = self.start_time + datetime.timedelta(seconds=start_pos)
        end_time = self.start_time + datetime.timedelta(seconds=end_pos)

        self.set_start_time(start_time.strftime("%H:%M:%S"))
        self.set_end_time(end_time.strftime("%H:%M:%S"))

        if start_pos != self.previous_start_pos:
            self.data_manager.change_start_time(int(start_time.timestamp()))
            self.previous_start_pos = start_pos

        else:
            self.data_manager.change_end_time(int(end_time.timestamp()))
            self.timeline_slider.end_handle_pos = end_pos  # Update the previous end position

        self.main_window.clear_content()
        self.main_window.create_navbar()

    def set_start_time(self, start_time: str) -> None:
        self.start_label.setText(f"Start Time: {start_time}")

    def set_end_time(self, end_time: str) -> None:
        self.end_label.setText(f"End Time: {end_time}")

    def update_times(self, start_time: datetime.datetime, end_time: datetime.datetime) -> None:
        self.start_time = start_time
        self.end_time = end_time
        self.setupTimes()
