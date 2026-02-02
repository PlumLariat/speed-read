from PySide6.QtCore import QRunnable, Slot, Signal, QObject
from file_processing import extract

class WorkerThread(QRunnable):
    def __init__(self, file_path: str) -> None:
        super().__init__()
        self.signals = WorkerSignals()
        self.file_path = file_path

    @Slot()
    def run(self):
        try:
            print("Starting!")
            text = extract(self.file_path)
            self.signals.result.emit(text)
            self.signals.finished.emit()
        except Exception as e:
            self.signals.error.emit(str(e))

class WorkerSignals(QObject):
    finished = Signal()
    error = Signal(str) 
    result = Signal(str)
        