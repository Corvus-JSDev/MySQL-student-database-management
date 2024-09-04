from PyQt6.QtWidgets import QApplication, QVBoxLayout, QLabel, QWidget, QLineEdit, QPushButton, QMainWindow, QTableWidget, QTableWidgetItem, QDialog, QComboBox, QToolBar
from PyQt6.QtGui import QAction, QIcon
import sys
import sqlite3
from pprint import pp
from contextlib import contextmanager

@contextmanager
def connect_to_database(database="database.db"):
	connection = sqlite3.connect(database)
	try:
		yield connection
	finally:
		connection.close()

class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()

		# Set window values
		self.setWindowTitle("Student Management System")
		width, height = 750, 500
		self.resize(width, height)
		self.setMinimumSize(500, 450)

		# Add menu items
		file_menu_item = self.menuBar().addMenu("&File")
		help_menu_item = self.menuBar().addMenu("&Help")
		edit_menu_item = self.menuBar().addMenu("&Edit")

		# Add sub-menu items
		add_student_subitem = QAction(QIcon("./icons/add.png"), "Add Student", self)
		add_student_subitem.triggered.connect(self.add_student)
		file_menu_item.addAction(add_student_subitem)

		about_subitem = QAction("About", self)
		help_menu_item.addAction(about_subitem)

		search_subitem = QAction(QIcon("./icons/search.png"), "Search", self)
		search_subitem.triggered.connect(self.search_students)
		edit_menu_item.addAction(search_subitem)

		# Add table
		self.table = QTableWidget()
		self.table.setColumnCount(4)
		self.table.setHorizontalHeaderLabels(("ID", "Name", "Course", "Contact"))
		self.table.verticalHeader().setVisible(False)  # Hide the index column on the left
		self.setCentralWidget(self.table)

		# Create toolbar
		toolbar = QToolBar()
		toolbar.setMovable(True)
		self.addToolBar(toolbar)
		toolbar.addAction(add_student_subitem)
		toolbar.addAction(search_subitem)


	def load_data(self):
		with connect_to_database("database.db") as connection:
			result = connection.execute("SELECT * FROM students")

			table = self.table
			table.setRowCount(0)  # Reset the table to prevent duplicate data
			for index_row, row_data in enumerate(result):
				table.insertRow(index_row)  # Create the row that the data will go into

				for index_column, data in enumerate(row_data):
					# Insert data at these coordinates
					table.setItem(index_row, index_column, QTableWidgetItem(str(data)))


	def add_student(self):
		InsertDialog().exec()


	def search_students(self):
		StudentSearch().exec()



class StudentSearch(QDialog):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Search For Student")
		grid = QVBoxLayout()
		width, height = 500, 300
		self.resize(width, height)

		# Create Widgets
		search_label = QLabel("Search by name")
		search_input = QLineEdit()
		search_input.setPlaceholderText("John Smith")

		submit_btn = QPushButton("Search")
		# submit_btn.clicked.connect(self.submit_search)

		# Place Widgets
		grid.addWidget(search_label)
		grid.addWidget(search_input)
		grid.addWidget(submit_btn)

		self.setLayout(grid)



class InsertDialog(QDialog):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Add Student")
		grid = QVBoxLayout()
		width, height = 500, 300
		self.resize(width, height)

		# Create widgets
		name_label = QLabel("Student\'s Name")
		self.name_input = QLineEdit()
		self.name_input.setPlaceholderText("John Smith")

		course_label = QLabel("Student\'s Course")
		self.course_input = QComboBox()
		self.course_input.addItems(["Biology", "Math", "Astronomy", "Physics", "English"])

		contact_label = QLabel("Student\'s Contact Info")
		self.contact_input = QLineEdit()
		self.contact_input.setPlaceholderText("John.Smith@school.com")

		submit_btn = QPushButton("Add Student")
		submit_btn.clicked.connect(self.register_student)
		self.output_msg = QLabel("")

		# Place widgets
		grid.addWidget(name_label)
		grid.addWidget(self.name_input)
		grid.addWidget(course_label)
		grid.addWidget(self.course_input)
		grid.addWidget(contact_label)
		grid.addWidget(self.contact_input)
		grid.addWidget(submit_btn)
		grid.addWidget(self.output_msg)


		self.setLayout(grid)


	def register_student(self):
		with connect_to_database("database.db") as connection:
			name = self.name_input.text().title()
			course = self.course_input.itemText(self.course_input.currentIndex())
			contact = self.contact_input.text()

			cursor = connection.cursor()
			# The ID for the student is added automatically by the database
			cursor.execute("INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)",
					   (name, course, contact))
			connection.commit()

			self.output_msg.setText(f"{name} has been added as a student")
			main_window.load_data()



app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())