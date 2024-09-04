from PyQt6.QtWidgets import QApplication, QVBoxLayout, QLabel, QWidget, QLineEdit, QPushButton, QMainWindow, QTableWidget
from PyQt6.QtGui import QAction
import sys
import sqlite3

class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()

		# Set window values
		self.setWindowTitle("Student Management System")
		width, height = 750, 500
		self.resize(width, height)

		# Add menu items
		file_menu_item = self.menuBar().addMenu("&File")
		help_menu_item = self.menuBar().addMenu("&Help")

		# Add sub-menu items
		file_menu_item.addAction(QAction("Add Student", self))
		help_menu_item.addAction(QAction("About", self))

		# Add table
		self.table = QTableWidget()
		self.table.setColumnCount(4)
		self.table.setHorizontalHeaderLabels(("ID", "Name", "Course", "Contact"))
		self.setCentralWidget(self.table)


	def load_data(self):
		tabel = self.table
		connection = sqlite3.connect("database.db")
		result = connection.execute("SELECT * FROM students")


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())