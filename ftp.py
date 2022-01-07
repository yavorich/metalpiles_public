from PyQt5.QtWidgets import \
    QDialog, QSpinBox, QLineEdit, QGroupBox, QGridLayout, QPushButton, QVBoxLayout, QHBoxLayout, QProgressBar, \
    QCheckBox, QPlainTextEdit, QButtonGroup


class FTPConfigWindow(QDialog):
    def __init__(self, parent = None):
        super(FTPConfigWindow, self).__init__(parent)
        self.create_config_boxes()
        self.create_config_buttons()
        self.create_progress_bar()

        # CheckBox that sets default FTP configurations
        self.disableCheckBox = QCheckBox('Set default FTP configuration')
        # self.disableCheckBox.toggled.connect(self.configBox.setDisabled)
        # self.disableCheckBox.toggled.connect(self.progressBarBox.setDisabled)
        self.disableCheckBox.toggled.connect(self.set_default_settings)
        # disableCheckBox.stateChanged

        main_layout = QGridLayout()
        main_layout.addWidget(self.disableCheckBox, 0, 0)
        main_layout.addWidget(self.configBox, 1, 0)
        main_layout.addWidget(self.configButtonsBox, 1, 1)
        main_layout.addWidget(self.progressBarBox, 2, 0, 1, 2)
        self.setLayout(main_layout)
        self.setWindowTitle('FTP config info')


    def create_config_boxes(self):
        '''
        Creates config line edit boxes (address, username, password)
        and default buttons
        '''
        self.configBox = QGroupBox('Config FTP info')

        # username, password and address textboxes
        addressBox = QLineEdit('address')
        addressBox.setObjectName('addressBox')
        usernameBox = QLineEdit('username')
        usernameBox.setObjectName('usernameBox')

        passwordBox = QLineEdit('username')
        passwordBox.setObjectName('addressBox')
        passwordBox.setEchoMode(QLineEdit.Password)

        # Implement a layout and set it to the GroupBox
        layout = QVBoxLayout()
        layout.addWidget(addressBox)
        layout.addWidget(usernameBox)
        layout.addWidget(passwordBox)
        # layout.addWidget(loadToFTPButton, 0, 1)

        self.configBox.setLayout(layout)

    def create_config_buttons(self):
        '''
        Creates config line edit boxes (address, username, password)
        and default buttons
        '''

        # button which is used fot FTP loading
        loadToFTPButton = QPushButton('Load to FTP')
        self.configButtonsBox = QGroupBox()
        # self.configButtonsBox.setFlat(True)
        layout = QVBoxLayout()
        layout.addWidget(loadToFTPButton)
        self.configButtonsBox.setLayout(layout)

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

    def set_default_settings(self, isChecked):
        '''
        Sets default config settings to configBox and set disabled all necessary widgets
        :param isChecked: checkbox isChecked condition
        '''
        echomode_initial_configs = {'address': QLineEdit.Normal, 'username': QLineEdit.Normal, 'password': QLineEdit.Password}
        echomode_default_configs = {'address': QLineEdit.Password, 'username': QLineEdit.Password, 'password': QLineEdit.Password}

        initial_configs = {'address': 'address', 'username': 'username', 'password': 'password'}
        default_configs = self.get_default_configs()

        # Define config variables depending on a checkbox
        configs = default_configs if isChecked else initial_configs
        echomode_configs = echomode_default_configs if isChecked else echomode_initial_configs


        print(configs)
        print(isChecked)
        # print(self.configBox.findChild(QLineEdit, 'usernameBox').setText)
        print()

        widgetType = 'Box'
        for qLineEdit in self.configBox.findChildren(QLineEdit):
            object_name = qLineEdit.objectName().split(widgetType)[0] #TODO: implement another iteration algorithm
            qLineEdit.setEchoMode(echomode_configs[object_name])
            qLineEdit.setText(configs[object_name])

        self.configBox.setDisabled(isChecked)
        self.progressBarBox.setDisabled(isChecked)


    def get_default_configs(self):
        '''
        Returns a dictionary with FTP configurations
        :return:
        '''
        return {'address': 'default_address', 'username': 'default_username', 'password': 'default_password'}
