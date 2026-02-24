from PySide6.QtCore import QRunnable, Slot, Signal, QObject
from file_processing import extract

class WorkerThread(QRunnable):
    def __init__(self, func, *args, **kwargs) -> None:
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @Slot()
    def run(self):
        try:
            out = self.func(*self.args, **self.kwargs)
            self.signals.result.emit(out)
        except Exception as e:
            self.signals.error.emit(str(e))
        finally:
            self.signals.finished.emit()

class WorkerSignals(QObject):
    finished = Signal()
    error = Signal(str) 
    result = Signal(str)
        