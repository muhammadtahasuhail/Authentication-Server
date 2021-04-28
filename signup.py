import socket
import sys
import json
from aes import AESCipher
from client import Client
from PyQt5.QtWidgets import (QLineEdit, QApplication, QWidget, QPushButton, 
                            QVBoxLayout, QHBoxLayout, QMessageBox)
 
class SignUpForm(QWidget):

    def __init__(self):

        super(SignUpForm, self).__init__()
        self.setupUi()

     
    def setupUi(self):
        self.setFixedSize(300, 200)
        self.setWindowTitle("Make a new account")
         
        self.Usernameedit = QLineEdit()
        self.Passwordedit = QLineEdit()
        self.confirmPasswordedit = QLineEdit()
        self.Passwordedit.setEchoMode(QLineEdit.Password)
        self.confirmPasswordedit.setEchoMode(QLineEdit.Password)
		
        self.confirmButton = QPushButton()
        self.cancelButton = QPushButton()
		
        self.confirmButton.clicked.connect(self.getSignUpValues)
        self.cancelButton.clicked.connect(lambda: self.close())

        self.confirmButton.setText("Confirm")
        self.cancelButton.setText("Cancel")
        self.Usernameedit.setPlaceholderText("Username")
        self.Passwordedit.setPlaceholderText("Password")
        self.confirmPasswordedit.setPlaceholderText("Confirm Password")
        self.confirmPasswordedit.returnPressed.connect(self.getSignUpValues)
         
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        vbox.addWidget(self.Usernameedit)
        vbox.addWidget(self.Passwordedit)
        vbox.addWidget(self.confirmPasswordedit)
        hbox.addWidget(self.cancelButton)
        hbox.addWidget(self.confirmButton)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

    def displayMessage(self, msg):
        QMessageBox.about(self, "Registration", msg)	
		
    def getSignUpValues(self):
    
        values = [self.Usernameedit.text(), self.Passwordedit.text(), self.confirmPasswordedit.text()]
        
        if values[1] == values[2]:
            status = self.registerClient(values)
            self.displayMessage(status)
            
        else:
            self.displayMessage('Passwords Donot Match!')
            
        self.close()
        
    def aesChallenge(self, message):

        key = 'ASD120KLO12OQN39'
        aes = AESCipher(key)
        return aes.encrypt(message)
        
    def registerClient(self, values):
    
        client = Client()
        client.register_credentials(values[0], values[1], values[2])
        to_send = client.get_credentials()
        to_send = json.dumps(to_send)

        skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        host, port = client.get_server_info()
        skt.connect((host, port))
        skt.sendall(bytes(to_send, encoding="utf-8"))
        
        to_encrypt = skt.recv(1024)
        
        encrypted = self.aesChallenge(to_encrypt.decode("utf-8"))

        skt.sendall(encrypted)
        
        received = skt.recv(1024)
        skt.close()
        return received.decode("utf-8") 
            
     
if __name__ == '__main__':

    import sys
    app = QApplication(sys.argv)
    mainWin = SignUpForm()
    mainWin.show()
    sys.exit(app.exec_())
