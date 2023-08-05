"""A simple script to demonstrate PyQt6."""

from __future__ import annotations

import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QLabel, QWidget


def main():
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle("Simple")
    window.setGeometry(300, 300, 300, 300)
    label = QLabel(window)
    label.setText("Hello World!")
    label.setGeometry(0, 0, 300, 300)
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
