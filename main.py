import sys,shutil,os,json
from pathlib import Path

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QMainWindow, QGridLayout, QWidget, QLabel,QSizePolicy

accepted_dir=os.environ.get('ACCEPTED_EMAILS')
rejected_dir=os.environ.get('REJECTED_EMAILS')
review_pending_dir=os.environ.get('REVIEW_PENDING')

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        layout=QGridLayout()

        yes_button = QPushButton("Accept Email")
        layout.addWidget(yes_button,6,0)

        no_button = QPushButton("Reject Email")
        layout.addWidget(no_button,6,1)

        exit_button = QPushButton("Exit")
        layout.addWidget(exit_button, 6, 3)

        yes_button.setCheckable(True)
        no_button.setCheckable(True)
        exit_button.setCheckable(True)
        yes_button.clicked.connect(self.accept_email)
        no_button.clicked.connect(self.reject_email)
        exit_button.clicked.connect(self.exit)
        yes_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        no_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        exit_button.setFixedWidth(yes_button.sizeHint().width()//2)



        widget=QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        recipient=''
        subject=''
        email_text=''
        self.recipient=QLabel(f'Recipient: {recipient}')
        self.subject=QLabel(f'Subject: {subject}')
        self.email_body=QLabel(email_text)
        layout.addWidget(self.recipient, 0,0)

        layout.addWidget(self.subject,1,0)

        recipient_font=self.recipient.font()
        recipient_font.setPointSize(15)
        self.recipient.setFont(recipient_font)

        subject_font=self.subject.font()
        subject_font.setPointSize(15)
        self.subject.setFont(subject_font)

        email_body_font=self.email_body.font()
        email_body_font.setPointSize(15)
        self.email_body.setFont(email_body_font)
        self.email_body.setWordWrap(True)
        layout.addWidget(self.email_body,2,0)

        layout.setRowStretch(0, 0) 
        layout.setRowStretch(1, 0)  
        layout.setRowStretch(2, 1)  


        file_list = [file for file in os.listdir(review_pending_dir)]
        self.current_index=0 
        self.emails=[]
        for file in file_list:
            json_data=self.read_contents(file)
            self.emails.append({
                "recipient": json_data[0],
                "subject": json_data[1],
                "body": json_data[2],
                "filename": file,
                })


        self.display_email(0)

    #sending candidate template to the accepted dir
    def accept_email(self):
        print("Email is ok to send off")
        file = self.emails[self.current_index]["filename"]
        review_pending_filepath=Path(review_pending_dir)/file
        accepted_filepath=Path(accepted_dir)/file
        shutil.copyfile(review_pending_filepath,accepted_filepath)

        if self.current_index < len(self.emails) - 1:
            self.current_index += 1
            self.display_email(self.current_index)
        else:
            self.recipient.setText("No more emails.")
            self.subject_label.setText("")
            self.email_body_label.setText("")

    #sending candidate template to the rejection dir
    def reject_email(self):
        print("Email needs to be reviewed")
        file = self.emails[self.current_index]["filename"]
        review_pending_filepath=Path(review_pending_dir)/file
        rejected_filepath=Path(rejected_dir)/file
        shutil.copyfile(review_pending_filepath,rejected_filepath)

        if self.current_index < len(self.emails) - 1:
            self.current_index += 1
            self.display_email(self.current_index)
        else:
            self.recipient.setText("No more emails.")
            self.subject_label.setText("")
            self.email_body_label.setText("")

    #reading contents of json file
    def read_contents(self,file):
        review_pending_filepath=Path(review_pending_dir)/file
        with open(review_pending_filepath, "r", encoding="utf-8") as f:
            data=json.load(f)

        recipient=data["recipient"]
        subject=data["subject"]
        email_body=data["email_body"]
        content=[recipient,subject,email_body]
        return content

    def display_email(self, index):
        email = self.emails[index]
        self.recipient.setText(f"Recipient: {email['recipient']}")
        self.subject.setText(f"Subject: {email['subject']}")
        self.email_body.setText(email['body'])
            
    #exit the viewer gracefully
    def exit(self):
        exit()

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
