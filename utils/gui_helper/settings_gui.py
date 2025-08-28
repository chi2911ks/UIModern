import os
from PyQt5.QtWidgets import QLineEdit, QCheckBox, QSpinBox, QDoubleSpinBox, QComboBox, QPlainTextEdit, QRadioButton, QWidget
from utils.json_handle.json_handle import JSONHandler
os.makedirs("data", exist_ok=True)
class SettingsGUI:
    def __init__(self, file_path="data\\settings.json", widget: QWidget=None):
        self.json_handle = JSONHandler(file_path)
        self.widget = widget
        self.__load_settings()
        self.__connect_settings()
    def __connect_settings(self):
        for ob in self.widget.findChildren((QLineEdit, QCheckBox, QRadioButton, QSpinBox, QDoubleSpinBox, QComboBox, QPlainTextEdit)):
            if isinstance(ob, QLineEdit):
                ob.textChanged.connect(self.__on_changed)
            elif isinstance(ob, QPlainTextEdit):
                ob.textChanged.connect(lambda o=ob: self.__on_changed(o.toPlainText()))
            elif isinstance(ob, QCheckBox):
                ob.stateChanged.connect(self.__on_changed)
            elif isinstance(ob, QRadioButton):
                ob.clicked.connect(self.__on_changed)
            elif isinstance(ob, (QSpinBox, QDoubleSpinBox)):
                ob.valueChanged.connect(self.__on_changed)
            elif isinstance(ob, QComboBox):
                ob.currentTextChanged.connect(self.__on_changed)
    def __on_changed(self, text):
        sender = self.widget.sender()
        object_name = sender.objectName()
        if object_name == "qt_spinbox_lineedit": return
        self.json_handle.update_json(object_name, text)
    def __load_settings(self):
        data = {}
        data = self.json_handle.read_json()
        childs = self.widget.findChildren((QLineEdit,  QCheckBox, QRadioButton, QSpinBox, QDoubleSpinBox, QComboBox, QPlainTextEdit))
        for ob in childs:
            object_wd = ob.objectName()
            if data and object_wd in data:
                if isinstance(ob, QLineEdit):
                    ob.setText(data[object_wd])
                elif isinstance(ob, QPlainTextEdit):
                    ob.setPlainText(data[object_wd])
                elif isinstance(ob, (QCheckBox, QRadioButton)):
                    ob.setChecked(data[object_wd])
                elif isinstance(ob, (QSpinBox, QDoubleSpinBox)):
                    ob.setValue(data[object_wd])
                elif isinstance(ob, QComboBox):
                    ob.setCurrentText(data[object_wd])