import sys

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QMainWindow, QGridLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        layout=QGridLayout()

        yes_button = QPushButton("Accept Email")
        layout.addWidget(yes_button,3,2)

        no_button = QPushButton("Reject Email")
        layout.addWidget(no_button,3,1)

        yes_button.setCheckable(True)
        no_button.setCheckable(True)
        yes_button.clicked.connect(self.accept_email)
        no_button.clicked.connect(self.reject_email)

        widget=QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def accept_email(self):
        print("Email is ok to send off")

    def reject_email(self):
        print("Email needs to be reviewed")
        
    def print_contents(self):
        return

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
