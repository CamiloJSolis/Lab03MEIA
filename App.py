import os.path
import sys
import pickle
from PyQt6.QtWidgets import (QMainWindow, QLineEdit, QPushButton, QFileDialog,
                             QApplication, QMessageBox, QTreeView, QTreeWidgetItem)
from PyQt6.uic import loadUi
from FrmCreate import FrmBook


class MainUI(QMainWindow):
    def __init__(self):
        super(MainUI, self).__init__()
        loadUi("Main.ui", self)

        # region Widgets Initialization
        self.le_path = self.findChild(QLineEdit, "le_path")
        self.tw_book_data = self.findChild(QTreeView, "tw_data")
        self.btn_create_save = self.findChild(QPushButton, "btn_create_save")
        self.btn_exit = self.findChild(QPushButton, "btn_exit")
        self.btn_query = self.findChild(QPushButton, "btn_query")

        self.btn_create_save.clicked.connect(self.btn_create_save_clicked)
        self.btn_exit.clicked.connect(self.exit_button_clicked)
        self.btn_query.clicked.connect(self.query_button_clicked)
        self.data = []
        # endregion

    def btn_create_save_clicked(self):
        if self.le_path.text() == "":
            book_form = FrmBook()
            book_form.exec()

            book_data = book_form.get_book_data()

            save_file, _ = QFileDialog.getSaveFileName(self, "Guardar Archivo", "", "")
            if save_file:
                save_file_path = save_file
                try:
                    if os.path.isdir(save_file_path):
                        with open(save_file_path, 'rb') as f:
                            try:
                                loaded_data = pickle.load(f)
                                if isinstance(loaded_data, list):
                                    self.data = [loaded_data]
                                else:
                                    self.data = []
                            except EOFError:
                                self.data = []
                    else:
                        self.data = []

                    self.data.append(book_data)

                    with open(save_file_path, 'ab') as f:
                        pickle.dump(book_data, f)
                    self.le_path.setText(save_file_path)
                except Exception as ex:
                    QMessageBox.critical(self, "Guardar Archivo", f"Ocurrió un error al abrir el archivo: {ex}")
        else:
            file_name = self.le_path.text()
            if file_name and os.path.exists(file_name):
                if os.path.exists(file_name):
                    book_form = FrmBook()
                    book_form.exec()
                    book_data = book_form.get_book_data()

                    try:
                        with open(file_name, 'rb') as f:
                            try:
                                loaded_data = pickle.load(f)
                                if isinstance(loaded_data, list) or isinstance(loaded_data, dict):
                                    self.data = [loaded_data]
                                else:
                                    self.data = []
                            except EOFError:
                                self.data = []

                        self.data.append(book_data)

                        with open(file_name, 'ab') as f:
                            pickle.dump(book_data, f)
                    except Exception as ex:
                        QMessageBox.critical(self, "Abrir Archivo", f"Ocurrió un error al abrir el archivo: {ex}")



    def query_button_clicked(self):
        file_path = self.le_path.text()
        if file_path and os.path.exists(file_path):
            try:
                with open(file_path, 'rb') as f:
                    self.data = []

                    while True:
                        try:
                            loaded_data = pickle.load(f)
                            if isinstance(loaded_data, dict) and loaded_data:
                                self.data.append(loaded_data)
                        except EOFError:
                            break

                self.tw_book_data.clear()

                for index, book in enumerate(self.data):
                    item = QTreeWidgetItem()

                    item.setText(0, str(index + 1))
                    item.setText(1, str(book.get('code')))
                    item.setText(2, str(book.get('title')))
                    item.setText(3, str(book.get('author')))
                    item.setText(4, str(book.get('school')))

                    self.tw_book_data.addTopLevelItem(item)
            except Exception as ex:
                QMessageBox.critical(self, "Consulta", f"Ocurrió un error al mostrar el archivo: {ex}")
        else:
            QMessageBox.critical(self, "Consulta", "No hay archivo cargado o el archivo no existe.")


    def exit_button_clicked(self):
        try:
            confirm = QMessageBox.question(self, "Confirmación de salida", "¿Está seguro que desea salir?",
                                           QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                           QMessageBox.StandardButton.No)
            if confirm == QMessageBox.StandardButton.Yes:
                self.close()
        except Exception as ex:
            QMessageBox.critical(self, "Cerrar aplicación", f"Ocurrió un error al cerrar el programa {ex}")


def main():
    app = QApplication(sys.argv)
    ui = MainUI()
    ui.show()

    try:
        app.exec()
    except Exception as ex:
        QMessageBox.critical("Error", f"Ocurrió un error al ejecutar la aplicación: {ex}")


main()
