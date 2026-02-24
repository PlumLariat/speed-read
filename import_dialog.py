from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QDialogButtonBox,
    QLabel,
    QProgressBar,
)

from PySide6.QtCore import QThreadPool, Slot
from PySide6.QtGui import QMovie

from worker_thread import WorkerThread

class ImportDialog(QDialog):
    def __init__(self, file_path: str, parent=None,) -> None:
        super().__init__(parent)
        self.file_path = file_path
        self.tesseractFinished = False

        self.thread_pool = QThreadPool()

        self.setWindowTitle("PDF Import")

        self.status_label = QLabel(
            "The file you entered has been detected as a PDF and must be converted to raw text to proceed."
        )
        self.pb = QProgressBar()
        self.pb.hide()

        self.loading_label = QLabel()
        self.spinner_animation = QMovie("assets/red_spinner.gif")
        self.loading_label.setMovie(self.spinner_animation)
        self.loading_label.hide()

        self.btn_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        self.btn_box.accepted.connect(self.on_ok_clicked)
        self.btn_box.rejected.connect(self.reject)

        # layouts
        self.import_layout = QVBoxLayout(self)
        self.bottom_row_layout = QHBoxLayout()

        # vertical
        self.import_layout.addWidget(self.status_label)
        self.import_layout.addWidget(self.pb)

        # horizontal
        self.bottom_row_layout.addWidget(self.loading_label)
        self.bottom_row_layout.addStretch(1)
        self.bottom_row_layout.addWidget(self.btn_box)

        self.import_layout.addLayout(self.bottom_row_layout)

    def on_ok_clicked(self):

        if not self.tesseractFinished:
            self.status_label.setText("Starting Tesseract extraction...")

            # In-Progress UI 
            self.pb.setRange(0,0)
            self.pb.show()
            self.loading_label.show()
            self.spinner_animation.start()

            ok_btn = self.btn_box.button(QDialogButtonBox.StandardButton.Ok)
            ok_btn.setEnabled(False)

            self.wt = WorkerThread(self.file_path)

            # connect thread signals
            self.wt.signals.finished.connect(self.tesseract_worker_finished)
            self.wt.signals.error.connect(self.tesseract_worker_error)
            self.wt.signals.result.connect(self.tesseract_worker_result)

            self.thread_pool.start(self.wt)
            return
        
        # close dialog, send the accept signal
        self.accept()

    @Slot()
    def tesseract_worker_finished(self):
        self.tesseractFinished = True
        self.spinner_animation.stop()
        self.loading_label.hide()
        self.pb.hide()

        ok_btn = self.btn_box.button(QDialogButtonBox.StandardButton.Ok)
        ok_btn.setEnabled(True)
        
        self.status_label.setText("Extraction complete. Press Ok to Continue.")

    @Slot(str)
    def tesseract_worker_result(self, text: str):
        print(text)

    @Slot(str)
    def tesseract_worker_error(self, msg: str):
        self.spinner_animation.stop()
        self.loading_label.hide()
        self.pb.hide()

        ok_btn = self.btn_box.button(QDialogButtonBox.StandardButton.Ok)
        ok_btn.setEnabled(True)

        self.status_label.setText(f"Extraction Failed: {msg}")


