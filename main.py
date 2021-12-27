from PyQt5.QtWidgets import QApplication

import validation
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    example_window = validation.ValidationWindow()
    example_window.show()
    sys.exit(app.exec_())