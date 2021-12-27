from PyQt5.QtWidgets import \
    QDialog, QSpinBox, QLineEdit, QGroupBox, QGridLayout, QPushButton, QVBoxLayout, QHBoxLayout

from ftp import FTPConfigWindow

class ValidationWindow(QDialog):
    def __init__(self, parent=None):
        super(ValidationWindow, self).__init__(parent)

        self.create_login_boxes()
        self.create_login_buttons()

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.loginBox)
        main_layout.addWidget(self.buttonsGroupBox)
        self.setLayout(main_layout)
        self.setWindowTitle('Login window')


    def create_login_boxes(self):
        '''
        Creates login line edit boxes
        '''
        self.loginBox = QGroupBox('Log in')
        usernameBox = QLineEdit('username')

        passwordBox = QLineEdit('Hello World!!!')
        passwordBox.setEchoMode(QLineEdit.Password)

        layout = QVBoxLayout()
        layout.addWidget(usernameBox)
        layout.addWidget(passwordBox)

        self.loginBox.setLayout(layout)

    def create_login_buttons(self):
        '''
        Creates login buttons and their behaviors
        '''
        self.buttonsGroupBox = QGroupBox()
        loginButton = QPushButton('Log in')
        loginButton.setDefault(True)
        loginButton.clicked.connect(self.lock_open)

        signupButton = QPushButton('Sign up')
        signupButton.setDefault(True)
        layout = QHBoxLayout()
        layout.addWidget(signupButton)
        layout.addWidget(loginButton)
        self.buttonsGroupBox.setLayout(layout)

    def close_open(self):
        ftpConfigWindow = FTPConfigWindow(self)
        self.done(0)
        ftpConfigWindow.show()

    def lock_open(self):
        ftpConfigWindow = FTPConfigWindow(self)
        ftpConfigWindow.exec()






