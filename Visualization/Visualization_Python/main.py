
import sys
from PyQt5.QtWidgets import QApplication

from gui.file_dialogs.file_selection_widget import FileSelectionWidget

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Open the file selection window
    file_selection_widget = FileSelectionWidget()
    file_selection_widget.show()

    sys.exit(app.exec_())
