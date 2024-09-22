import os
import shutil

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog, QMessageBox, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from utils.data_manager import DataManager
from gui.main_window import MainWindow

class FileSelectionWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.sl_file = None
        self.csv_file = None  # CSV file variable

        self.setWindowTitle("Select Required Files")
        self.setGeometry(400, 200, 600, 300)  # Set window size and position
        self.setStyleSheet(self.get_stylesheet())  # Apply custom styles
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Title Label
        title_label = QLabel("Please select the required files to continue:")
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Row for SL JSON file
        sl_layout = QHBoxLayout()
        sl_label = QLabel("SL File:  ")
        self.sl_file_input = QLineEdit()
        self.sl_file_input.setReadOnly(True)
        sl_button = QPushButton("Browse")
        sl_button.clicked.connect(self.select_sl_file)
        sl_layout.addWidget(sl_label)
        sl_layout.addWidget(self.sl_file_input)
        sl_layout.addWidget(sl_button)

        # Row for CSV file
        csv_layout = QHBoxLayout()  # Layout for the CSV file
        csv_label = QLabel("CSV File:")  # Label changed to CSV
        self.csv_file_input = QLineEdit()
        self.csv_file_input.setReadOnly(True)
        csv_button = QPushButton("Browse")
        csv_button.clicked.connect(self.select_csv_file)  # Function to select CSV file
        csv_layout.addWidget(csv_label)
        csv_layout.addWidget(self.csv_file_input)
        csv_layout.addWidget(csv_button)

        # Proceed button
        self.proceed_button = QPushButton("Proceed")
        self.proceed_button.setEnabled(False)
        self.proceed_button.clicked.connect(self.proceed)

        # Add rows to the layout
        layout.addLayout(sl_layout)
        layout.addLayout(csv_layout)  # Add CSV layout
        layout.addWidget(self.proceed_button, alignment=Qt.AlignCenter)

        # Set spacing and margins
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        self.setLayout(layout)

    def select_sl_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "Select SL JSON File", "", "JSON Files (*.json);;All Files (*)")
        if file:
            self.sl_file = file
            self.sl_file_input.setText(file.split('/')[-1])
            self.check_files_selected()

    def select_csv_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "Select CSV File", "", "CSV Files (*.csv);;All Files (*)")
        if file:
            # Copy destination - 'data' folder within the project
            destination_dir = os.path.join(os.getcwd(), 'data')  # Get path to the data folder
            if not os.path.exists(destination_dir):
                os.makedirs(destination_dir)  # Create the folder if it doesn't exist

            # Define the paths for the old and new files
            base_name = 'logs.csv'
            destination_file = os.path.join(destination_dir, base_name)
            temp_file = os.path.join(destination_dir, 'temp_logs.csv')

            try:
                # First, copy the selected file to a temporary location
                shutil.copy(file, temp_file)
                print(f"File copied to temporary location: {temp_file}")

                # Remove the old file if it exists
                if os.path.exists(destination_file):
                    os.remove(destination_file)
                    print(f"Old file removed: {destination_file}")

                # Rename the temporary file to the desired name
                os.rename(temp_file, destination_file)
                print(f"Temporary file renamed to: {destination_file}")

                # Update input line with the file name
                self.csv_file = destination_file
                self.csv_file_input.setText(destination_file.split('/')[-1])  # Show the file name saved in the folder

                # Check if both files are selected
                self.check_files_selected()

            except Exception as e:
                # Display an error message box and print the exception details
                QMessageBox.critical(self, "Error", f"An error occurred while handling the file: {e}")
                print(f"Exception details: {e}")

                # Clean up by removing the temporary file if it was created
                if os.path.exists(temp_file):
                    os.remove(temp_file)
                    print(f"Temporary file removed: {temp_file}")

    def check_files_selected(self):
        if self.sl_file and self.csv_file:  # Check if both files are selected
            self.proceed_button.setEnabled(True)

    def proceed(self):
        if not self.sl_file or not self.csv_file:
            QMessageBox.critical(self, "Error", "Both files are required!")
            return

        # Use the copied files in the process
        data_manager = DataManager('data/chip_data.json', self.sl_file, self.csv_file)
        main_window = MainWindow(data_manager)
        main_window.showMaximized()

        self.close()

    def get_stylesheet(self):
        """Return QSS stylesheet for styling the widget."""
        return """
            QWidget {
                background-color: #f0f4f7;
                font-family: Arial;
            }
            QLabel {
                color: #333;
                font-size: 12pt;
            }
            QLineEdit {
                background-color: #fff;
                border: 2px solid #b0c4de;
                padding: 4px;
                border-radius: 5px;
            }
            QPushButton {
                background-color: #87ceeb;
                color: #fff;
                border: none;
                padding: 8px 16px;
                font-size: 12pt;
                border-radius: 5px;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
            QPushButton:hover {
                background-color: #00bfff;
            }
            QPushButton:pressed {
                background-color: #1e90ff;
            }
        """
