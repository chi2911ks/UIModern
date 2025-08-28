from typing import Dict
import uuid
from PyQt5.QtWidgets import QMainWindow, QApplication, QHeaderView, QPushButton, QComboBox, QMenu
from PyQt5.QtCore import Qt, pyqtSlot, QEventLoop, QTimer

from GUI.mainwindow_ui import Ui_MainWindow
from GUI import resources_rc
from control.work_thread import WorkThread
from utils.gui_helper.animation_sidebar import AnimationSideBar
from utils.gui_helper.settings_gui import SettingsGUI
from utils.gui_helper.table_view import TableViewHelper
from utils.gui_helper.title_bar import TitleBar

class App(QMainWindow, TitleBar, SettingsGUI):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        SettingsGUI.__init__(self, widget=self.ui.settings_page)
        AnimationSideBar(self.ui.navFrame)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.show()
        self.ui.titleFrame.mousePressEvent = self.mousePressEvent_
        self.ui.titleFrame.mouseMoveEvent = self.mouseMoveEvent_
        self.settings = self.ui
        self.table_helper = TableViewHelper(["emulator", "Nhiệm vụ", "Trạng thái", "#"], self.ui.tableView)
        self.model = self.table_helper.getModel()
        self.ui.tableView.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.ui.tableView.horizontalHeader().setSectionResizeMode(3, QHeaderView.Fixed)
        self.ui.tableView.setColumnWidth(2, 300)
        self.ui.tableView.setColumnWidth(3, 100)
        self.__list_thread: Dict[str, WorkThread] = {}
        self.testting()
        self.ui.tableView.contextMenuEvent = self.contextMenuTableView
        self.ui.tableView.selectionModel().selectionChanged.connect(self.on_row_selected)
    def sleep(self, duration):
        loop = QEventLoop()
        QTimer.singleShot(int(duration*1000), loop.quit)
        loop.exec_()
    def on_row_selected(self, selected, deselected):
        selected_rows = set(index.row() for index in self.ui.tableView.selectionModel().selectedRows())
        self.ui.label_selected.setText("<p><span style=\" font-weight:600; color:#0000ff;\">Đã chọn: </span><span style=\" font-weight:600;\">%s</span></p>"%len(selected_rows))
    def contextMenuTableView(self, event):
        menu = QMenu()
        action_start = menu.addAction("Bắt đầu")
        action_start.triggered.connect(self.actionStart)
        action_stop = menu.addAction("Kết thúc")
        action_stop.triggered.connect(self.actionStop)
        menu.exec_(event.globalPos())
    def actionStart(self):
        rows = [index.row() for index in self.ui.tableView.selectionModel().selectedRows()]
        for row in rows:
            self.handle_button_click(row)
            self.sleep(0.5)
    def actionStop(self):
        rows = [index.row() for index in self.ui.tableView.selectionModel().selectedRows()]
        for row in rows:
            task_id = self.model.data(self.model.index(row, 0), Qt.UserRole)
            button: QPushButton = self.ui.tableView.indexWidget(self.model.index(row, 3))
            button.setText("Bắt đầu")
            thread = self.__list_thread.get(task_id)
            if thread:
                thread.terminate()
                del self.__list_thread[task_id]
                self.sleep(0.5)
    def handle_button_click(self, row):
        button: QPushButton = self.ui.tableView.indexWidget(self.model.index(row, 3))
        combo: QComboBox = self.ui.tableView.indexWidget(self.model.index(row, 1))
        #lấy task_id ra để tạo key - value cho __list_thread
        task_id = self.model.data(self.model.index(row, 0), Qt.UserRole)
        if button.text() == "Bắt đầu":
            button.setText("Kết thúc")
            print("Bắt đầu task_id:", task_id)
            self.__list_thread[task_id] = WorkThread(row, combo.currentText(), self)
            self.__list_thread[task_id].status.connect(self.table_helper.set_item_text)
            self.__list_thread[task_id].start()
        else:
            print("Kết thúc task_id:", task_id)
            button.setText("Bắt đầu")
            # kết thúc theo đúng task id nên việc xoá row khng ảnh hưởng, nhưng nếu xoá row đang chạy thì vẫn sẽ có lỗi 
            # à đm xoá đi thì kiểu gì cũng lỗi hết tất cả vì khi xoá đi một row thì nó sẽ đẩy các row còn lại ở dưới lên nên đang chạy thì kiểu gì cũng lỗi à
            # nếu ai khôn thì tư duy ra thêm nhé lười lắm rồi =))
            thread = self.__list_thread.get(task_id)
            if thread:
                thread.terminate()
                del self.__list_thread[task_id]
    def testting(self):
        
        for emulator in ["1", "2", "3", "4", "5"]:
            row = self.table_helper.insert_row()
            self.table_helper.create_combobox(row, 1, ["Nhiệm vụ 1", "Nhiệm vụ 2", "Nhiệm vụ 3"])
            # bind cho mỗi button một handle_button_click khác nhau và truyền thêm tham số row
            self.table_helper.create_button(row, 3, self.handle_button_click)
            # lưu task_id bằng setData, để nếu có làm chức năng xoá row thì không bị lỗi khi kill-thread
            task_id = str(uuid.uuid4())
            self.model.setData(self.model.index(row, 0), task_id, Qt.UserRole)
            self.table_helper.set_item_text(row, 0, emulator)
            self.table_helper.set_item_text(row, 2, "Chưa bắt đầu")
    @pyqtSlot()
    def on_homeBtn_clicked(self):
        self.ui.homeBtn.setChecked(True)
        self.ui.settingsBtn.setChecked(False)
        self.ui.contactBtn.setChecked(False)
        self.ui.helpBtn.setChecked(False)
        self.ui.main_stacked_widget.setCurrentIndex(0)
    @pyqtSlot()
    def on_settingsBtn_clicked(self):
        self.ui.homeBtn.setChecked(False)
        self.ui.settingsBtn.setChecked(True)
        self.ui.contactBtn.setChecked(False)
        self.ui.helpBtn.setChecked(False)
        self.ui.main_stacked_widget.setCurrentIndex(1)
    @pyqtSlot()
    def on_contactBtn_clicked(self):
        self.ui.homeBtn.setChecked(False)
        self.ui.settingsBtn.setChecked(False)
        self.ui.contactBtn.setChecked(True)
        self.ui.helpBtn.setChecked(False)
        self.ui.main_stacked_widget.setCurrentIndex(2)
    @pyqtSlot()
    def on_helpBtn_clicked(self):
        self.ui.homeBtn.setChecked(False)
        self.ui.settingsBtn.setChecked(False)
        self.ui.contactBtn.setChecked(False)
        self.ui.helpBtn.setChecked(True)
        self.ui.main_stacked_widget.setCurrentIndex(3)
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    main = App()
    sys.exit(app.exec_())