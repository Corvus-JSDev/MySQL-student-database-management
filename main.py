from PyQt6.QtWidgets import QApplication, QVBoxLayout, QLabel, QWidget, QLineEdit, QPushButton, QMainWindow
from PyQt6.QtGui import QAction
import sys

class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Student Management System")

		# Add menu items
		file_menu_item = self.menuBar().addMenu("&File")
		help_menu_item = self.menuBar().addMenu("&Help")

		# Add sub menu items
		file_menu_item.addAction(QAction("Add Student", self))
		help_menu_item.addAction(QAction("About", self))



app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec())