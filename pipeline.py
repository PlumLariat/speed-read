from PySide6.QtCore import QObject, Signal, QThreadPool, Slot

class Pipeline(QObject):
    done = Signal(object)
    failed = Signal(str)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.serial_pool = QThreadPool()
        self.serial_pool.setMaxThreadCount(1)

        self.parallel_pool = QThreadPool()
        self.parallel_pool.setMaxThreadCount(max(2, QThreadPool.globalInstance().maxThreadCount()))

    
