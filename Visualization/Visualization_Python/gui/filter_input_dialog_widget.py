from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton,
                             QComboBox, QFormLayout, QMessageBox)
from PyQt5.QtCore import Qt

from utils.types_name import AREAS, UNIT_MAP


class FilterInputDialogWidget(QDialog):

    def __init__(self, filter_type: str, parent=None) -> None:
        """Initialize the dialog with a filter name."""
        super().__init__(parent)
        self.filter_type = filter_type  # Store the filter name to customize the dialog
        self.parent = parent  # Reference to the parent widget
        self.initUI()

    def initUI(self) -> None:
        """Initialize the user interface for the dialog."""
        self.setWindowTitle(f'Enter values for {self.filter_type}')
        self.setFixedSize(600, 450)  # Set a fixed size for the dialog
        self.setStyleSheet("""
            QDialog {
                background-color: #f9f9f9;
                border-radius: 12px;
            }
            QLabel {
                font-weight: bold;
                color: #333;
            }
            QLineEdit, QComboBox {
                border: 1px solid #ddd;
                border-radius: 6px;
                padding: 8px;
                font-size: 14px;
            }
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                padding: 12px;
                border-radius: 6px;
                font-size: 16px;
                cursor: pointer;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #004494;
            }
            QFormLayout {
                margin: 20px;
                row-wrap: wrap;
            }
            QVBoxLayout {
                spacing: 10px;
            }
        """)

        self.setLayout(QVBoxLayout())  # Set the main layout of the dialog
        self.form_layout = QFormLayout()
        self.layout().addLayout(self.form_layout)  # Add the form layout to the main layout

        self.setup_form_fields()  # Set up form fields based on filter_type
        self.setup_buttons()  # Add Apply and Cancel buttons

    def setup_form_fields(self) -> None:
        """Create and add form fields based on the filter name."""
        if self.filter_type == self.parent.filter_types.Cluster.name:
            self.chip_input = QComboBox(self)
            self.chip_input.addItems(['0'])  # Currently only 0 available
            self.form_layout.addRow('Chip:', self.chip_input)
            self.die_input = QComboBox(self)
            self.die_input.addItems(['Die 1', 'Die 2'])
            self.form_layout.addRow('Die:', self.die_input)
            self.quad_input = QComboBox(self)
            self.quad_input.addItems(['HW', 'NE', 'SW', 'SE'])  # Human-readable options
            self.form_layout.addRow('Quad:', self.quad_input)
            self.row_input = QComboBox(self)
            self.row_input.addItems([str(i) for i in range(8)])  # 0-7 for row
            self.form_layout.addRow('Row:', self.row_input)
            self.column_input = QComboBox(self)
            self.column_input.addItems([str(i) for i in range(8)])  # 0-7 for column
            self.form_layout.addRow('Column:', self.column_input)
        elif self.filter_type == self.parent.filter_types.Quad.name:
            self.chip_input = QComboBox(self)
            self.chip_input.addItems(['0'])  # Currently only 0 available
            self.form_layout.addRow('Chip:', self.chip_input)
            self.die_input = QComboBox(self)
            self.die_input.addItems(['Die 1', 'Die 2'])
            self.form_layout.addRow('Die:', self.die_input)
            self.quad_input = QComboBox(self)
            self.quad_input.addItems(['HW', 'NE', 'SW', 'SE'])  # Human-readable options for quad
            self.form_layout.addRow('Quad:', self.quad_input)
        elif self.filter_type == self.parent.filter_types.ThreadId.name:
            self.tid_input = QLineEdit(self)
            self.tid_input.setPlaceholderText('Enter TID number')
            self.form_layout.addRow('TID:', self.tid_input)
        elif self.filter_type == self.parent.filter_types.Io.name:
            self.inout_input = QComboBox(self)
            self.inout_input.addItems(['in', 'out'])
            self.form_layout.addRow('Select In/Out:', self.inout_input)
        elif self.filter_type == self.parent.filter_types.Area.name:
            self.area_input = QComboBox(self)
            self.area_input.addItems(AREAS.keys())
            self.form_layout.addRow('Select Area:', self.area_input)
        elif self.filter_type == self.parent.filter_types.Unit.name:
            self.unit_input = QComboBox(self)
            self.unit_input.addItems(list(UNIT_MAP.keys()))
            self.form_layout.addRow('Select Unit:', self.unit_input)

    def setup_buttons(self) -> None:
        """Create and add buttons to the dialog."""
        button_layout = QVBoxLayout()

        self.apply_button = QPushButton('Apply', self)
        self.apply_button.clicked.connect(self.apply_filter)
        button_layout.addWidget(self.apply_button)

        self.cancel_button = QPushButton('Cancel', self)
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        self.layout().addLayout(button_layout)  # Add buttons to the main layout

    def apply_filter(self) -> None:
        """Validate and apply the filter based on user input."""
        values = None

        if self.filter_type == self.parent.filter_types.Cluster.name:
            chip_value = (self.chip_input.currentText())  # Convert chip value to integer
            die_value = (self.die_input.currentIndex())  # Index corresponds to Die 1 => 0, Die 2 => 1
            quad_value = (self.quad_input.currentIndex())  # Index corresponds to HW => 0, NE => 1, SW => 2, SE => 3
            row_value = (self.row_input.currentText())  # Row as integer
            column_value = (self.column_input.currentText())  # Column as integer

            values = [int(chip_value), die_value, quad_value, int(row_value), int(column_value)]

        elif self.filter_type == self.parent.filter_types.Quad.name:
            chip_value = int(self.chip_input.currentText())  # Convert chip value to integer
            die_value = self.die_input.currentIndex()
            quad_value = self.quad_input.currentIndex()
            values = (chip_value, die_value, quad_value)

        elif self.filter_type == self.parent.filter_types.ThreadId.name:
            tid_value = self.tid_input.text().strip()  # Ensure no leading/trailing spaces
            if tid_value:  # Make sure the value is not empty
                values = int(tid_value)
        elif self.filter_type == self.parent.filter_types.Io.name:
            values = self.inout_input.currentText()

        elif self.filter_type == self.parent.filter_types.Area.name:
            area_value = self.area_input.currentText()
            values = area_value

        elif self.filter_type == self.parent.filter_types.Unit.name:
            unit_value = self.unit_input.currentText()
            values = unit_value

        # Verify that all values are non-empty or non-None
        # if None not in values and "" not in values:
        self.parent.apply_filter(self.filter_type, values)
        self.accept()
        # else:
        #     QMessageBox.warning(self, 'Invalid Input', 'Please enter all required values.')