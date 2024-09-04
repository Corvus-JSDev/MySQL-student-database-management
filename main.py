from PyQt6.QtWidgets import QApplication, QVBoxLayout, QLabel, QWidget, QLineEdit, QPushButton, QMainWindow, QTableWidget, QTableWidgetItem
from PyQt6.QtGui import QAction
import sys
import sqlite3
from pprint import pp
from contextlib import contextmanager

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
		self.table.verticalHeader().setVisible(False)  # Hide the index column on the left
		self.setCentralWidget(self.table)


	@contextmanager
	def connect_to_database(self, database):
		connection = sqlite3.connect(database)
		try:
			yield connection
		finally:
			connection.close()

	def load_data(self):
		with self.connect_to_database("database.db") as connection:
			result = connection.execute("SELECT * FROM students")

			table = self.table
			table.setRowCount(0)  # Reset the table to prevent duplicate data
			for index_row, row_data in enumerate(result):
				table.insertRow(index_row)  # Create the row that the data will go into

				for index_column, data in enumerate(row_data):
					# Insert data at these coordinates
					table.setItem(index_row, index_column, QTableWidgetItem(str(data)))




app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())