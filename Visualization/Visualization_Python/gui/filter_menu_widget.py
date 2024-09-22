from PyQt5.QtWidgets import QMenu, QLabel, QWidgetAction, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtCore import Qt
from gui.filter_input_dialog_widget import FilterInputDialogWidget
from typing import Optional, Dict, List, Union


class FilterMenuWidget(QMenu):
    def __init__(self,filter_types,parent=None):
        super().__init__('Filter ▼', parent)
        self.parent = parent
        self.filters_action = []
        self.filter_types = filter_types
        self.initUI()

    def initUI(self) -> None:
        self.setStyleSheet("""
            QMenu {
                background-color: #2d2d2d;
                border: 1px solid #000;
            }
            QMenu::item:selected {
                background-color: #555;
            }
        """)

        self.hovered.connect(lambda: self.parent.setCursor(Qt.PointingHandCursor))

        # Define filter options
        self.filters = {
            self.filter_types.Cluster.name: ['Die', 'Quad', 'Row', 'Column'],
            self.filter_types.Area.name: ['LNB', 'CBU', 'MCU', 'TCU', 'Ecore', 'PCIe/Host IF', 'BMT', 'HBM', 'D2D'],
            self.filter_types.Unit.name: ['bmt', 'pcie', 'CBUS INJ', 'CBUS CLT', 'NFI INJ', 'NFI CLT', 'IRAQ', 'EQ', 'HBM', 'TCU', 'IQR',
                     'IQD', 'BIN', 'LNB'],
            self.filter_types.ThreadId.name: ['TID'],
            self.filter_types.Io.name: ['in', 'out'],
            self.filter_types.Quad.name: ['HW', 'NE', 'SW', 'SE']
        }

        self.actions = {}
        for filter_type, options in self.filters.items():
            if filter_type in self.filters_action:
                widget = QLabel(f'{filter_type}   ✓')
            else:
                widget = QLabel(filter_type)

            widget.setStyleSheet("padding: 8px 20px; color: white; background-color: #2d2d2d;")
            action = QWidgetAction(self)
            action.setDefaultWidget(widget)
            self.addAction(action)

            # Connect action trigger to filter selection
            widget.mouseReleaseEvent = lambda event, name=filter_type: self.filter_selected(name)

            self.actions[filter_type] = widget

        self.add_clear_filters_button()
        self.update_filter_Text()

    def add_clear_filters_button(self) -> None:
        """Add a button to clear all filters."""
        clear_button = QPushButton('Clear Filters')
        clear_button.setStyleSheet("""
            QPushButton {
                padding: 8px 20px;
                color: white;
                background-color: #d9534f; /* Red color for emphasis */
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #c9302c; /* Darker red for hover effect */
            }
        """)
        clear_button.clicked.connect(self.clear_all_filters)

        # Create a QWidgetAction for the button
        action = QWidgetAction(self)
        action.setDefaultWidget(clear_button)
        self.addAction(action)

    def filter_selected(self, filter_type: str) -> None:
        """Handle filter selection and update the styles."""
        if filter_type in self.filters_action:
            # Remove fiRlter and update styles
            self.filters_action.remove(filter_type)
            self.update_filter_Text()
            self.parent.filter_removal(filter_type)
        else:
            # Add filter and show the input dialog
            self.show_input_dialog(filter_type)

    def update_filter_Text(self) -> None:
        """Update the styles of the menu items based on the selected filters."""
        for filter_type, widget in self.actions.items():
            if filter_type in self.filters_action:
                widget.setText(f"{filter_type}  ✓")
            else:
                widget.setText(filter_type)

    def show_input_dialog(self, filter_type: str) -> None:
        """Show the input dialog for the selected filter."""
        dialog = FilterInputDialogWidget(filter_type, self)
        dialog.exec_()

    def apply_filter(self, filter_type: str, values: list) -> None:
        """Apply the filter with the given name and values."""
        print(f'Filter {filter_type} applied with values: {values}')
        if self.parent is not None:
            self.filters_action.append(filter_type)
            self.update_filter_Text()
            self.parent.change_filter(filter_type, values)

    def clear_all_filters(self) -> None:
        """Clear all selected filters and update the menu."""
        self.filters_action.clear()
        self.update_filter_Text()
        self.parent.clear_all_filters()
