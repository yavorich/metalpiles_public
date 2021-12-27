from PyQt5.QtWidgets import \
    QDialog, QSpinBox, QLineEdit, QGroupBox, QGridLayout, QPushButton, QVBoxLayout, QHBoxLayout, QProgressBar, \
    QCheckBox, QPlainTextEdit


class FTPConfigWindow(QDialog):
    def __init__(self, parent = None):
        super(FTPConfigWindow, self).__init__(parent)

        self.create_config_boxes()
        self.create_progress_bar()

        disableCheckBox = QCheckBox('Set default FTP configuration')
        disableCheckBox.toggled.connect(self.configBox.setDisabled)
        disableCheckBox.toggled.connect(self.progressBarBox.setDisabled)

        main_layout = QGridLayout()
        main_layout.addWidget(disableCheckBox, 0, 0)
        main_layout.addWidget(self.configBox, 1, 0)
        main_layout.addWidget(self.progressBarBox, 2, 0)
        self.setLayout(main_layout)
        self.setWindowTitle('FTP config info')


    def create_config_boxes(self):
        '''
        Creates config line edit boxes (address, username, password)
        and default buttons
        '''
        self.configBox = QGroupBox('Config FTP info')

        usernameBox = QLineEdit('username')
        passwordBox = QLineEdit('username')
        passwordBox.setEchoMode(QLineEdit.Password)

        loadToFTPButton = QPushButton('Load to FTP')


        layout = QGridLayout()
        layout.addWidget(usernameBox, 0, 0)
        layout.addWidget(passwordBox, 1, 0)
        layout.addWidget(loadToFTPButton, 0, 1)

        self.configBox.setLayout(layout)

    def create_progress_bar(self):
        '''
        Creates the progress bar that depicts FTP loading process
        '''
        self.progressBarBox = QGroupBox()

        progressBar = QProgressBar()
        progressBar.setRange(0, 10_000)
        progressBar.setValue(0)

        layout = QVBoxLayout()
        layout.addWidget(progressBar)

        self.configBox.setLayout(layout)

    def create_list_box(self):
        '''
        Create textbox with a list of label data
        '''

        self.listGroupBox = QGroupBox()
        listTextEdit = QPlainTextEdit()

        layout = QVBoxLayout()
        layout.addWidget(listTextEdit)
        self.listGroupBox.setLayout(layout)


    def load_to_ftp(self):
        '''
        Loads label data to FTP server
        '''
        pass