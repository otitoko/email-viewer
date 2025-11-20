import sys
import os
import shutil

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QMainWindow, QGridLayout, QWidget

accepted_dir=os.environ.get('ACCEPTED_EMAILS')
rejected_dir=os.environ.get('REJECTED_EMAILS')
review_pending_dir=os.environ.get('REVIEW_PENDING')

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

        file_list = [file for file in os.listdir(f"{REVIEW_PENDING}")]

        email_text=read_contents(file)
        email_body=QLabel(email_text)
        layout.addWidget(email_body,2,1)


    def accept_email(self):
        print("Email is ok to send off")
        shutil.copyfile(review_pending_dir/file,accepted_dir/file)

    def reject_email(self):
        print("Email needs to be reviewed")
        shutil.copyfile(review_pending_dir/file,rejected_dir/file)

    def read_contents(file):
        file_path=open(f"{review_pending}/{file}")
        content=file_path.read()
        return content

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
