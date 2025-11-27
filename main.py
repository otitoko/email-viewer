import sys
import os
import shutil
from pathlib import Path

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QMainWindow, QGridLayout, QWidget, QLabel

accepted_dir=os.environ.get('ACCEPTED_EMAILS')
rejected_dir=os.environ.get('REJECTED_EMAILS')
review_pending_dir=os.environ.get('REVIEW_PENDING')

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        layout=QGridLayout()

        yes_button = QPushButton("Accept Email")
        layout.addWidget(yes_button,3,0)

        no_button = QPushButton("Reject Email")
        layout.addWidget(no_button,3,1)

        exit_button = QPushButton("Exit")
        layout.addWidget(exit_button, 3, 3)

        yes_button.setCheckable(True)
        no_button.setCheckable(True)
        exit_button.setCheckable(True)
        yes_button.clicked.connect(self.accept_email)
        no_button.clicked.connect(self.reject_email)
        exit_button.clicked.connect(self.exit)

        widget=QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        file_list = [file for file in os.listdir(review_pending_dir)]

        for file in file_list:
            email_text=self.read_contents(file)
            email_body=QLabel(email_text)
            email_body.setWordWrap(True)
            layout.addWidget(email_body,2,0)


    def accept_email(self,file):
        print("Email is ok to send off")
        review_pending_filepath=Path(review_pending_dir)/file
        accepted_filepath=Path(accepted_dir)/file
        shutil.copyfile(review_pending_filepath,accepted_filepath)

    def reject_email(self,file):
        print("Email needs to be reviewed")
        review_pending_filepath=Path(review_pending_dir)/file
        rejected_filepath=Path(rejected_dir)/file
        shutil.copyfile(review_pending_filepath,rejected_filepath)

    def read_contents(self,file):
        review_pending_filepath=Path(review_pending_dir)/file
        file_path=open(review_pending_filepath)
        content=file_path.read()
        return content

    def exit(self):
        exit()

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
