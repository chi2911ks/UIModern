from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, pyqtSlot
class TitleBar:
    @pyqtSlot()
    def on_closeBtn_clicked(self): self.close()
    @pyqtSlot()
    def on_minimizeBtn_clicked(self): self.showMinimized()
    @pyqtSlot()
    def on_maximizeBtn_clicked(self):
        if self.isMaximized():
            self.showNormal()
            self.ui.maximizeBtn.setIcon(QIcon(":/nav/icons/square-svgrepo-com.svg"))
        else:
            self.showMaximized()
            self.ui.maximizeBtn.setIcon(QIcon(":/nav/icons/minimize-svgrepo-com.svg"))
    def mousePressEvent_(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPos = event.globalPos()
        self.mousePressEvent(event)
    
    def mouseMoveEvent_(self, event):
        if self.dragPos and event.buttons() == Qt.LeftButton:
            # di chuyển cửa sổ cha
            parent = self.window()
            diff = event.globalPos() - self.dragPos
            parent.move(parent.pos() + diff)
            self.dragPos = event.globalPos()
        self.mouseMoveEvent(event)