import sys, random

from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
    QMenu,
    QMenuBar,
    QLabel,
    QProgressBar,
    QPushButton,
    QSpinBox,
    QWidget,
    QGridLayout
)
from PySide6.QtGui import QIcon, QAction
from PySide6 import QtCore

from layout_colorwidget import Color

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

        # define all necessary components

        self.word_display = QLabel("Upload a file to get started.")
        self.pb = QProgressBar()
        self.wpm_control = QSpinBox()
        self.play_button = QPushButton("Play")
        self.pause_button = QPushButton("Pause")
        self.upload_file_button = QPushButton("Upload Text")

        # connect signals and slots and other set-up vars
        self.play_button.clicked.connect(self.play)
        self.pause_button.clicked.connect(self.pause)
        self.upload_file_button.clicked.connect(self.uploadFile)

        # disable controls without file upload
        self.play_button.setEnabled(False)
        self.pause_button.setEnabled(False)

        # Define the layout
        layout = QGridLayout()
        layout.addWidget(self.word_display, 0, 0, 4, 7, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.play_button, 4, 0)
        layout.addWidget(self.pause_button, 4, 1)
        layout.addWidget(self.pb, 4, 2, 1, 3)
        layout.addWidget(self.wpm_control, 4, 5, 1, 2)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.setMenuBar(self.__init_menu_bar())

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
    
    def __init_menu_bar(self) -> QMenuBar:
        mb = QMenuBar()
        
        fm = QMenu(title="File")

        em = QMenu(title="Edit")
        
        hm = QMenu(title="Help")

        mb.addMenu(fm)
        mb.addMenu(em)
        mb.addMenu(hm)

        return mb


if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()
    window.show()

    sys.exit(app.exec())