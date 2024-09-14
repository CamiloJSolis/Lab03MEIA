import os.path
import sys
import pickle
from PyQt6.QtWidgets import (QMainWindow, QWidget, QGridLayout, QLineEdit, QPushButton, QFormLayout,
                             QFileDialog, QApplication, QMessageBox, QTreeView, QDialog, QTreeWidgetItem)
from PyQt6.uic import loadUi
from FrmCreate import FrmBook


class MainUI(QMainWindow):
    def __init__(self):
        super(MainUI, self).__init__()
        loadUi("Main.ui", self)

        # region Widgets Initialization
        self.le_path = self.findChild(QLineEdit, "le_path")
        self.tw_book_data = self.findChild(QTreeView, "tw_book_data")
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

            save_file, _ = QFileDialog.getSaveFileName(self, "Guardar Archivo", "/home", ".dat")
            if save_file:
                save_file_path = save_file
                try:
                    with open(save_file_path, 'ab') as f:
                        pickle.dump(book_form.get_book_data(), f)
                    self.le_path.setText(save_file_path)
                except Exception as ex:
                    QMessageBox.critical(self, "Guardar Archivo", f"Ocurrió un error al abrir el archivo: {ex}")
        else:
            file_name, _ = QFileDialog.getOpenFileName(self, "Abrir Archivo", "/home", "All Files (*.*)")
            if file_name:
                if os.path.exists(file_name):
                    try:
                        with open(file_name, 'rb') as f:
                            self.data = pickle.load(f)
                            self.le_path.setText(file_name)
                    except Exception as ex:
                        QMessageBox.critical(self, "Abrir Archivo", f"Ocurrió un error al abrir el archivo: {ex}")
                        
    def query_button_clicked(self):
        file_path = self.le_path.text()
        if file_path and os.path.exists(file_path):
            try:
                with open(self.le_path, 'rb') as f:
                    pickle.dump(self.data, f)
                self.fill_tree_widget()
            except Exception as ex:
                QMessageBox.critical(self, "Consulta", f"Ocurrió un error al mostrar el archivo: {ex}")
            else:
                QMessageBox.critical(self, "Consulta", "No hay archivo cargado o el archivo no existe.")

    def fill_tree_widget(self):
        self.tw_book_data.clear()

        for d, book in enumerate(self.data):
            data = QTreeWidgetItem(book)

            data.setText(0, str(d + 1))
            data.setText(1, book[1])
            data.setText(2, book[2])
            data.setText(3, book[3])
            data.setText(4, book[4])

            self.tw_book_data.insertTopLevelItem(data)

        self.tw_book_data.resizeColumnToContents(0)

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
