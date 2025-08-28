from typing import List
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QTableView, QPushButton, QComboBox
class TableViewHelper:
    def __init__(self, column_labels: List[str], tableView: QTableView):
        self.column_labels = column_labels
        self.tableView = tableView
        self.__model = QStandardItemModel(0, len(self.column_labels))
        self.__model.setHorizontalHeaderLabels(self.column_labels)
        self.tableView.setModel(self.__model)
    def getModel(self):
        return self.__model
    def set_item_text(self, row: int, col: int, text: str):
        text = str(text)
        item = self.__model.item(row, col)
        if item is None:
            self.__model.setItem(row, col, QStandardItem(text))
        else:
            item.setText(text)
    def insert_row(self):
        row = self.__model.rowCount()
        self.__model.insertRow(row)
        return row
    def create_combobox(self, row, column, items: List[str]):
        combo = QComboBox()
        combo.addItems(items)
        self.tableView.setIndexWidget(self.__model.index(row, column), combo)
    def create_button(self, row, column, callback):
        button = QPushButton("Bắt đầu")
        button.clicked.connect(lambda checked, r=row: callback(r))
        self.tableView.setIndexWidget(self.__model.index(row, column), button)