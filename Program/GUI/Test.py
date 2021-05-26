from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys

class UserLogin(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("Respirate")
        self.register = False
        self.label = QLabel()
        self.label.setText("Name")
        self.passLabel = QLabel()
        self.passLabel.setText("Password")
        self.boxLayout = QVBoxLayout()
        self.nameText = QLineEdit()
        self.passwordText = QLineEdit()
        self.acceptButton = QPushButton()
        self.acceptButton.setText("Accept")
        self.acceptButton.clicked.connect(self.accept)
        self.acceptButton.clicked.connect(self.close)
        self.createButton = QPushButton()
        self.createButton.setText("New user")
        self.createButton.clicked.connect(self.OnRegister)
        self.createButton.clicked.connect(self.accept)
        self.createButton.clicked.connect(self.close)
        self.rejectButton = QPushButton()
        self.rejectButton.setText("Cancel")
        self.rejectButton.clicked.connect(self.reject)
        self.boxLayout.addWidget(self.label)
        self.boxLayout.addWidget(self.nameText)
        self.boxLayout.addWidget(self.passLabel)
        self.boxLayout.addWidget(self.passwordText)
        self.boxLayout.addWidget(self.acceptButton)
        self.boxLayout.addWidget(self.createButton)
        self.boxLayout.addWidget(self.rejectButton)
        self.setLayout(self.boxLayout)
    def OnAccept(self):
        return self.nameText.text(), self.passwordText.text(), self.register
    def OnRegister(self):
        self.register = True

if (__name__ == "__main__"):
    app = QApplication(sys.argv)
    dialog = UserLogin()
    dialog.exec_()
    if dialog.result() == 1:
        name, password = dialog.OnAccept()
        print(name + password)