from PyQt5.QtWidgets import  QPushButton, QFrame
from PyQt5.QtCore import Qt, QPropertyAnimation
class AnimationSideBar:
    def __init__(self, frame: QFrame):
        self.frame = frame
        self.animation = QPropertyAnimation(self.frame, b"maximumWidth")
        self.animation.setDuration(150)
        self.buttons = {}
        for ob in self.frame.findChildren((QPushButton)):
            self.buttons[ob] = ob.text()
        for btn in self.buttons.keys():
            btn.setText("")
        # self.enter_old = self.frame.enterEvent
        # self.leave_old = self.frame.leaveEvent
        self.frame.enterEvent = self.enterEvent_
        self.frame.leaveEvent = self.leaveEvent_
    # Hover mở rộng
    def enterEvent_(self, event):
        self.animation.stop()
        self.animation.setStartValue(self.frame.width())
        self.animation.setEndValue(180)
        self.animation.start()
        for btn, text in self.buttons.items():
            btn.setText(text)
        # self.enter_old(event)
    # Rời chuột thu nhỏ
    def leaveEvent_(self, event):
        self.animation.stop()
        self.animation.setStartValue(self.frame.width())
        self.animation.setEndValue(60)
        self.animation.start()
        for btn in self.buttons.keys():
            btn.setText("")
        # self.leave_old(event)