import sys, random

from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
    QLabel,
    QPushButton,
    QWidget,
    QVBoxLayout
)
from PySide6.QtGui import QIcon
from PySide6 import QtCore

def txt_file_to_list(filepath: str) -> list[str]:
    
    with open(filepath) as file:
        f_str = file.read()
        token_list = f_str.split()

    return token_list


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Speed Reader")
        self.setWindowIcon(QIcon('./assets/lightning.png'))
        self.resize(800, 600)

        central = QWidget(self)
        self.setCentralWidget(central)

        self.text = QLabel(
            "No File Loaded. Press \'Upload Text\'",
            alignment=QtCore.Qt.AlignmentFlag.AlignCenter
        )

        self.play_button = QPushButton("Play")
        self.pause_button = QPushButton("Pause")
        self.upload_file_button = QPushButton("Upload Text")

        self.main_layout = QVBoxLayout(central)
        self.main_layout.addWidget(self.text)
        self.main_layout.addWidget(self.play_button)
        self.main_layout.addWidget(self.pause_button)
        self.main_layout.addWidget(self.upload_file_button)

        self.play_button.clicked.connect(self.play)
        self.pause_button.clicked.connect(self.pause)
        self.upload_file_button.clicked.connect(self.uploadFile)

        # disable controls without file upload
        self.play_button.setEnabled(False)
        self.pause_button.setEnabled(False)

    @QtCore.Slot()
    def play(self):
        print("I should play now")

    @QtCore.Slot()
    def pause(self):
        print("I should pause now")

    @QtCore.Slot()
    def uploadFile(self):
        f_name, _ = QFileDialog.getOpenFileName(
            self,
            "Open Text File",
            ".",
            "(*.txt)"
        )

        if f_name:
            self.text.setText(f"Selected file: {f_name}.")
            t_list = txt_file_to_list(f_name)
            print(t_list)
            self.play_button.setEnabled(True)
            self.pause_button.setEnabled(True)
        


if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()
    window.show()

    sys.exit(app.exec())