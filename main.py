from PyQt6.QtCore import Qt
import mysql.connector
import sys
from contextlib import contextmanager

from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMainWindow, QTableWidget, \
	QTableWidgetItem, QDialog, QComboBox, QToolBar, QStatusBar, QGridLayout, QMessageBox

import os
from dotenv import load_dotenv

load_dotenv()
SQL_USER = os.getenv("SQL_USER")
SQL_PASS = os.getenv("SQL_PASS")
SQL_URL = os.getenv("SQL_URL")
SQL_TABLE = os.getenv("SQL_TABLE")


@contextmanager
def connect_to_database():
	connection = mysql.connector.connect(host=SQL_URL, user=SQL_USER, password=SQL_PASS, database=SQL_TABLE)

	try:
		yield connection
	finally:
		if connection.is_connected():
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
		add_student_subitem.triggered.connect(self.add_student_dialog)
		file_menu_item.addAction(add_student_subitem)

		about_subitem = QAction("About", self)
		help_menu_item.addAction(about_subitem)
		about_subitem.triggered.connect(self.about)

		search_subitem = QAction(QIcon("./icons/search.png"), "Search", self)
		search_subitem.triggered.connect(self.search_dialog)
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

		# Create status bar
		self.statusbar = QStatusBar()
		self.setStatusBar(self.statusbar)

		# Detect a cell click
		self.table.cellClicked.connect(self.cell_clicked)


	def cell_clicked(self):
		# Create buttons
		edit_btn = QPushButton("Edit")
		edit_btn.clicked.connect(self.edit_dialog)
		delete_record_btn = QPushButton("Delete")
		delete_record_btn.clicked.connect(self.delete_dialog)

		# Clear the statusbar
		children = self.findChildren(QPushButton)
		if children:
			for child in children:
				self.statusbar.removeWidget(child)

		# Add the widgets
		self.statusbar.addWidget(edit_btn)
		self.statusbar.addWidget(delete_record_btn)


	def load_data(self):
		with connect_to_database() as connection:
			cursor = connection.cursor()
			cursor.execute("SELECT * FROM students")
			result = cursor.fetchall()

			table = self.table
			table.setRowCount(0)  # Reset the table to prevent duplicate data
			for index_row, row_data in enumerate(result):
				table.insertRow(index_row)  # Create the row that the data will go into

				for index_column, data in enumerate(row_data):
					# Insert data at these coordinates
					table.setItem(index_row, index_column, QTableWidgetItem(str(data)))


	def add_student_dialog(self):
		AddStudentDialog().exec()

	def search_dialog(self):
		SearchDialog().exec()

	def edit_dialog(self):
		EditDialog().exec()

	def delete_dialog(self):
		DeleteDialog().exec()

	def about(self):
		AboutDialog().exec()



class AboutDialog(QMessageBox):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("About Page")
		message = """
This app was created to test out and get familiar with the PyQt lib.

This app is NOT meant for actual real world use.

If you would like, please feel free to steal this code.
It is available for download at:
https://github.com/Corvus-JSDev/student-database-management"""
		self.setText(message)


class EditDialog(QDialog):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Edit Student Data")
		grid = QVBoxLayout()
		width, height = 500, 300
		self.resize(width, height)

		row_index = main_window.table.currentRow()
		#                        coordinates: row, column index
		self.student_id = main_window.table.item(row_index, 0).text()
		student_name = main_window.table.item(row_index, 1).text()
		course_name = main_window.table.item(row_index, 2).text()
		student_contact = main_window.table.item(row_index, 3).text()

		# Create widgets
		name_label = QLabel("Student\'s Name")
		self.name_input = QLineEdit(student_name)

		course_label = QLabel("Student\'s Course")
		self.course_input = QComboBox()
		self.course_input.addItems(["Biology", "Math", "Astronomy", "Physics", "English"])
		self.course_input.setCurrentText(course_name)

		contact_label = QLabel("Student\'s Contact Info")
		self.contact_input = QLineEdit(student_contact)

		submit_btn = QPushButton("Update")
		submit_btn.clicked.connect(self.update_data)
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


	def update_data(self):
		name = self.name_input.text()
		course = self.course_input.itemText(self.course_input.currentIndex())
		contact = self.contact_input.text()
		student_id = self.student_id

		with connect_to_database() as connection:
			cursor = connection.cursor()
			cursor.execute("UPDATE students SET name = %s, course = %s, contact = %s WHERE id = %s",
					   (name, course, contact, student_id))
			connection.commit()

		self.output_msg.setText("Update Successful")
		main_window.load_data()


class DeleteDialog(QDialog):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Delete Student")
		grid = QGridLayout()
		width, height = 300, 150
		self.resize(width, height)

		self.row_index = main_window.table.currentRow()
		self.student_name = main_window.table.item(self.row_index, 1).text()
		self.student_id = main_window.table.item(self.row_index, 0).text()

		confirm_msg = QLabel(f"Are you sure you want to delete all of {self.student_name}\'s information?")
		cancel_btn = QPushButton("Cancel")
		cancel_btn.clicked.connect(self.close)
		delete_btn = QPushButton("Delete")
		delete_btn.clicked.connect(self.delete_student)

		grid.addWidget(confirm_msg, 0, 0, 1, 2)
		grid.addWidget(cancel_btn, 1, 1)
		grid.addWidget(delete_btn, 1, 0)
		self.setLayout(grid)


	def delete_student(self):
		with connect_to_database() as connection:
			cursor = connection.cursor()
			cursor.execute("DELETE FROM students WHERE id = %s", (self.student_id, ))
			connection.commit()

		main_window.load_data()
		self.close()

		# Confirmation window
		confirm_widget = QMessageBox()
		confirm_widget.setWindowTitle("Student Deleted")
		confirm_widget.setText(f"{self.student_name} has been successfully deleted")
		confirm_widget.exec()


class SearchDialog(QDialog):
	def __init__(self):
		super().__init__()
		# Set window title and size
		self.setWindowTitle("Search Student")
		self.resize(300, 200)

		# Create layout and input widget
		layout = QVBoxLayout()
		search_label = QLabel("Search Student\n(First-name Last-Name)")
		layout.addWidget(search_label)
		self.student_name = QLineEdit()
		self.student_name.setPlaceholderText("Name")
		layout.addWidget(self.student_name)
		self.output_msg = QLabel("")
		layout.addWidget(self.output_msg)

		# Create button
		button = QPushButton("Search")
		button.clicked.connect(self.search)
		layout.addWidget(button)

		self.setLayout(layout)

	def search(self):
		name = self.student_name.text().title()

		with connect_to_database() as connection:
			cursor = connection.cursor()
			cursor.execute("SELECT * FROM students WHERE name = %s", (name,))

			result = cursor.fetchall()
			if result:
				self.output_msg.setText("Success, Student Found!")
			else:
				self.output_msg.setText("NO student found")

			items = main_window.table.findItems(name, Qt.MatchFlag.MatchFixedString)
			for item in items:
				main_window.table.item(item.row(), 1).setSelected(True)


class AddStudentDialog(QDialog):
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
		with connect_to_database() as connection:
			name = self.name_input.text().title()
			course = self.course_input.itemText(self.course_input.currentIndex())
			contact = self.contact_input.text()

			cursor = connection.cursor()
			# The ID for the student is added automatically by the database
			cursor.execute("INSERT INTO students (name, course, contact) VALUES (%s, %s, %s)",
					   (name, course, contact))
			connection.commit()

		self.output_msg.setText(f"{name} has been added as a student")
		main_window.load_data()



if __name__ == "__main__":
	app = QApplication(sys.argv)
	main_window = MainWindow()
	main_window.show()
	main_window.load_data()
	sys.exit(app.exec())