from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt

class InfoDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Simulator Instructions")  # Set the title of the dialog
        self.setGeometry(300, 300, 600, 400)  # Set the initial size and position of the dialog

        # Improve the dialog's design with a stylesheet
        self.setStyleSheet("""
            QDialog {
                background-color: #f0f0f0;  # Light gray background
                border-radius: 10px;  # Rounded corners
            }
            QLabel {
                font-size: 14px;  # Set the font size for labels
                color: #333;  # Dark gray text color
            }
            QPushButton {
                background-color: #4CAF50;  # Green background for buttons
                color: white;  # White text color
                font-size: 14px;  # Font size for buttons
                padding: 10px;  # Padding inside buttons
                border-radius: 5px;  # Rounded corners for buttons
            }
            QPushButton:hover {
                background-color: #45a049;  # Darker green on hover
            }
        """)

        layout = QVBoxLayout()  # Vertical layout for the dialog

        # Instructions text with added margins between lines using HTML
        instructions = """
        <h2 style="color: #2980b9;">Simulator Instructions</h2>
        <p style="color: #2c3e50; font-size: 15px; margin-bottom: 20px;">
        <span style="font-weight: bold;">•</span> To move to the next layer, click on the corresponding element.<br><br>
        <span style="font-weight: bold;">•</span> Right-click on any element to view its logs.<br><br>
        <span style="font-weight: bold;">•</span> Colored elements indicate they contain logs.<br><br>
        <span style="font-weight: bold;">•</span> Use the toolbar to navigate between Host Interface, DIE1, DIE2, and more.<br><br>
        <span style="font-weight: bold;">•</span> Click "Filter" to open the filter menu and refine your view.
        </•
        """
        self.label = QLabel(instructions)  # Create a label for the instructions
        self.label.setWordWrap(True)  # Allow text to wrap within the label
        self.label.setAlignment(Qt.AlignTop)  # Align text to the top
        self.label.setTextFormat(Qt.RichText)  # Support for HTML formatting

        layout.addWidget(self.label)  # Add the label to the layout

        button_layout = QHBoxLayout()  # Horizontal layout for buttons
        self.close_button = QPushButton("Close")  # Create a close button
        self.close_button.clicked.connect(self.close)  # Connect button click to close the dialog
        button_layout.addStretch(1)  # Add stretchable space before the button
        button_layout.addWidget(self.close_button)  # Add the close button to the layout
        layout.addLayout(button_layout)  # Add button layout to the main layout

        self.setLayout(layout)  # Set the main layout for the dialog

        # Center the dialog on the parent window
        self.setWindowModality(Qt.ApplicationModal)  # Make the dialog modal
        self.move(self.parent().x() + (self.parent().width() - self.width()) // 2,
                  self.parent().y() + (self.parent().height() - self.height()) // 2)
