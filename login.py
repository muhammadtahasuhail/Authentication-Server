import socket
import sys
import json
from client import Client
from PyQt5.QtWidgets import (QLineEdit, QApplication, QWidget, QPushButton, 
                            QVBoxLayout, QHBoxLayout, QMessageBox)
 
class LoginForm(QWidget):

    def __init__(self):
	
        super(LoginForm, self).__init__()
        self.values = None
        self.login()


    def login(self):
	
        self.setFixedSize(300, 200)
        self.setWindowTitle("Login")
         
        self.Usernameedit = QLineEdit()
        self.Passwordedit = QLineEdit()
        self.Passwordedit.setEchoMode(QLineEdit.Password)
         
        self.confirmButton = QPushButton()
        self.cancelButton = QPushButton()
        self.confirmButton.clicked.connect(self.getLoginValues)
        self.cancelButton.clicked.connect(lambda: self.close())
 
        self.confirmButton.setText("Login")
        self.cancelButton.setText("Cancel")
        self.Usernameedit.setPlaceholderText("Username")
        self.Passwordedit.setPlaceholderText("Password")
        self.Passwordedit.returnPressed.connect(self.getLoginValues)
         
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        vbox.addWidget(self.Usernameedit)
        vbox.addWidget(self.Passwordedit)
        hbox.addWidget(self.cancelButton)
        hbox.addWidget(self.confirmButton)
        vbox.addLayout(hbox)
        self.setLayout(vbox)	

    def displayMessage(self, msg):
        QMessageBox.about(self, "Verification", msg)	
        
    def getLoginValues(self):
        
        values = [self.Usernameedit.text(), self.Passwordedit.text()]
        
        status = self.verifyCredentials(values)
        self.displayMessage(status)
        self.close()
        
        
    def verifyCredentials(self, values):
    
        client = Client()
        client.set_credentials(values[0], values[1])
        to_send = client.get_credentials()
        to_send = json.dumps(to_send)

        skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        received = None

        host, port = client.get_server_info()
        skt.connect((host, port))
        skt.sendall(bytes(to_send, encoding="utf-8"))
        
        received = skt.recv(1024)

        skt.close()
        return received.decode("utf-8") 
             
if __name__ == '__main__':

    import sys
    app = QApplication(sys.argv)
    mainWin = LoginForm()
    mainWin.show()
    sys.exit(app.exec_())
