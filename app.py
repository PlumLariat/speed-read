import sys

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
from PySide6.QtCore import QTimer, Slot, Qt
from word_list import WordList

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Speed Reader")
        self.setWindowIcon(QIcon('./assets/lightning.png'))
        self.resize(800, 600)

        # Non-GUI application variables
        self.word_list = WordList()

        self.timer = QTimer()
        self.timer.timeout.connect(self.timer_tick)
        self.timer_interval = 200

        # define and setup all necessary components 
        self.word_display = QLabel("Upload a file to get started.")
        self.word_display_font = self.word_display.font()
        self.word_display_font.setPointSize(32)
        self.word_display.setFont(self.word_display_font)

        self.prog_bar = QProgressBar()
        self.prog_bar.setMinimum(0)
        self.prog_bar.setTextVisible(False)

        self.wpm_control = QSpinBox()
        self.wpm_control.setRange(1,500)
        self.wpm_control.setValue(self.timer_interval)
        self.wpm_control.setSingleStep(10)
        self.wpm_control.valueChanged.connect(self.wpm_changed)


        self.play_button = QPushButton("Play")
        self.pause_button = QPushButton("Pause")

        # connect signals and slots and other set-up vars
        self.play_button.clicked.connect(self.play)
        self.pause_button.clicked.connect(self.pause)

        # disable controls before a file upload
        self.play_button.setEnabled(False)
        self.pause_button.setEnabled(False)

        # Define the layout, place components
        layout = QGridLayout()
        layout.addWidget(self.word_display, 0, 0, 4, 7, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.play_button, 4, 0)
        layout.addWidget(self.pause_button, 4, 1)
        layout.addWidget(self.prog_bar, 4, 2, 1, 3)
        layout.addWidget(self.wpm_control, 4, 5, 1, 2)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.setMenuBar(self.__init_menu_bar())

    @Slot()
    def play(self):
        if self.word_list.complete:
            self.word_list.reset()
            self.prog_bar.setValue(self.word_list.cur_index)
            self.word_display.setText(self.word_list.get_current_word())

        self.play_button.setEnabled(False)
        self.timer.setInterval(self.timer_interval) # 1 second intervals
        self.timer.start()

    @Slot()
    def pause(self):
        self.play_button.setEnabled(True)
        self.timer.stop()

    @Slot()
    def timer_tick(self):
        if not self.word_list.complete:
            self.word_list.next()
            self.word_display.setText(self.word_list.get_current_word())
            self.prog_bar.setValue(self.word_list.cur_index)
        else:
            self.pause()


    @Slot(int)
    def wpm_changed(self, value: int) -> int:
        # go from wpm to milisecond
        self.timer_interval

    def upload_file_action(self):
        f_name, _ = QFileDialog.getOpenFileName(
            self,
            "Open Text File",
            ".",
            "(*.txt)"
        )

        if f_name:
            self.word_list = WordList()
            self.word_list.init_from_txt_file(f_name)
            self.word_display.setText(self.word_list.get_current_word())
            self.play_button.setEnabled(True)
            self.pause_button.setEnabled(True)
            self.prog_bar.setMaximum(self.word_list.remaining)
    
    def __init_menu_bar(self) -> QMenuBar:
        mb = QMenuBar()
        
        fm = QMenu("File", self)
        open_action: QAction = QAction("Open", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.upload_file_action)
        fm.addAction(open_action) # type: ignore

        

        em = QMenu(title="Edit")
        
        hm = QMenu(title="Help")

        mb.addMenu(fm)
        mb.addMenu(em)
        mb.addMenu(hm)

        return mb
    
def wpm_to_ms(words: int) -> int:
    '''Get the time in microseconds required to display one word at requested words per minute'''
    return int(60_000.0 / words)




if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()
    window.show()

    sys.exit(app.exec())