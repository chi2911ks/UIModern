from PyQt5.QtCore import QThread, pyqtSignal
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app import App
class WorkThread(QThread):
    finished = pyqtSignal(int, str)
    status = pyqtSignal(int, int, str)
    def __init__(self, row: int, task: str, main_window: 'App'):
        super().__init__()
        self.row = row
        self.task = task
        self.main_window = main_window
        self.delay = self.main_window.settings.delaySP.value()
    def run(self):
        for i in range(int(self.delay)):
            self.status.emit(self.row, 2, f"Đang thực hiện {self.task} random: {i}")
            self.sleep(1)