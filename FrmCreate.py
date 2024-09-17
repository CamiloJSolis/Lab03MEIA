from PyQt6.QtWidgets import (QLineEdit, QPushButton, QMessageBox, QComboBox, QDialog)
from PyQt6.uic import loadUi


class FrmBook(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("NewEntry.ui", self)

        # region Widgets initialization
        self.le_code = self.findChild(QLineEdit, "le_code")
        self.le_title = self.findChild(QLineEdit, "le_title")
        self.le_author = self.findChild(QLineEdit, "le_author")
        self.cmbx_school = self.findChild(QComboBox, "cmbx_school")
        self.btn_save_book = self.findChild(QPushButton, "btn_save_book")

        self.btn_save_book.clicked.connect(self.save_button_clicked)
        # endregion

        self.book_data = {}

    def save_button_clicked(self):
        try:
            code = self.le_code.text()
            title = self.le_title.text()
            author = self.le_author.text()
            school = self.cmbx_school.currentText()

            if not code or not title or not author:
                QMessageBox.critical(self, "Advertencia", "Todos los campos deben ser llenados")
                return

            self.book_data = {
                "code": code,
                "title": title,
                "author": author,
                "school": school
            }

            self.accept()
        except Exception as ex:
            QMessageBox.critical(self, "Error", f"Ocurrió un error al guardar el archivo: {ex}")

    def get_book_data(self):
        return self.book_data
