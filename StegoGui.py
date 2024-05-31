from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QGridLayout, QFileDialog
from PyQt5.QtWidgets import QLineEdit, QCheckBox, QTextEdit, QDesktopWidget, QAction, QDialog, QVBoxLayout
from PyQt5.QtGui import QIcon, QFont
import sys, os
from StegoAlgorithm import hideDataToImage, extractDataFromImage
import StyleSheets


class CustomDialog(QDialog):
    def __init__(self, title, message, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setStyleSheet(StyleSheets.dialogStyle)
        if title == "Help Content":
            self.setFixedSize(500, 270)
        elif title == "About":
            self.setFixedSize(400, 180)

        layout = QVBoxLayout()
        self.setLayout(layout)
        message_label = QLabel(message)
        message_label.setWordWrap(True)
        layout.addWidget(message_label)

        button = QPushButton('OK')
        button.setStyleSheet(StyleSheets.buttonHideExtractStyle)
        button.clicked.connect(self.accept)
        layout.addWidget(button)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        """
        Initializes the user interface. Sets up the main window, widgets, layouts, and styles.
        
        Parameters:
        None

        Returns:
        None
        """
        self.setWindowTitle('Steganography App')
        base_path = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
        icon_path = os.path.join(base_path, 'icon.ico')
        self.setWindowIcon(QIcon(icon_path))
        self.setFixedSize(800, 270)

        self.centerWindow()
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        grid_layout = QGridLayout()
        central_widget.setLayout(grid_layout)
        
        font = QFont()
        font.setPointSize(9)
        QApplication.instance().setFont(font)
        
        # Menu Bar
        menubar = self.menuBar()
        menubar.setStyleSheet(StyleSheets.menuBarStyle)

        # File Menu
        file_menu = menubar.addMenu('File')
        clear_action = QAction('Clear', self)
        clear_action.triggered.connect(self.clearFields)
        file_menu.addAction(clear_action)
        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Help Menu
        help_menu = menubar.addMenu('Help')
        help_content_action = QAction('Help Content...', self)
        help_content_action.triggered.connect(self.showHelpContent)
        help_menu.addAction(help_content_action)
        about_action = QAction('About...', self)
        about_action.triggered.connect(self.showAbout)
        help_menu.addAction(about_action)

        # Input Image Path
        input_image_label = QLabel('Input Image Path:')
        self.inputImagePath = QLineEdit()
        self.inputImagePath.setMinimumWidth(200)
        self.inputImagePath.setStyleSheet(StyleSheets.pathFieldStyle)
        self.input_image_button = QPushButton('Choose File')
        self.input_image_button.setStyleSheet(StyleSheets.buttonChooseFileStyle)
        self.input_image_button.setMinimumHeight(10)
        self.input_image_button.clicked.connect(lambda: self.openFileDialog(self.inputImagePath, 'file'))
        grid_layout.addWidget(input_image_label, 0, 0)
        grid_layout.addWidget(self.inputImagePath, 0, 1)
        grid_layout.addWidget(self.input_image_button, 0, 2)

        # Hidden File Path
        self.hidden_file_label = QLabel('Hidden File Path:')
        self.hiddenFilePath = QLineEdit()
        self.hiddenFilePath.setMinimumWidth(200)
        self.hiddenFilePath.setStyleSheet(StyleSheets.pathFieldStyle)
        self.hidden_file_button = QPushButton('Choose File')
        self.hidden_file_button.setStyleSheet(StyleSheets.buttonChooseFileStyle)
        self.hidden_file_button.setMinimumHeight(10)
        self.hidden_file_button.clicked.connect(lambda: self.openFileDialog(self.hiddenFilePath, 'file'))
        grid_layout.addWidget(self.hidden_file_label, 1, 0)
        grid_layout.addWidget(self.hiddenFilePath, 1, 1)
        grid_layout.addWidget(self.hidden_file_button, 1, 2)

        # Output Image Path
        self.output_image_label = QLabel('Output Image Path:')
        self.outputImagePath = QLineEdit()
        self.outputImagePath.setMinimumWidth(200)
        self.outputImagePath.setStyleSheet(StyleSheets.pathFieldStyle)
        self.output_image_button = QPushButton('Choose File')
        self.output_image_button.setStyleSheet(StyleSheets.buttonChooseFileStyle)
        self.output_image_button.setMinimumHeight(10)
        self.output_image_button.clicked.connect(lambda: self.openFileDialog(self.outputImagePath, 'save'))
        grid_layout.addWidget(self.output_image_label, 2, 0)
        grid_layout.addWidget(self.outputImagePath, 2, 1)
        grid_layout.addWidget(self.output_image_button, 2, 2)

        # Password
        password_label = QLabel('Password:')
        self.password = QLineEdit()
        self.password.setMinimumWidth(200)
        self.password.setStyleSheet(StyleSheets.pathFieldStyle)
        self.password.setEchoMode(QLineEdit.Password)
        grid_layout.addWidget(password_label, 3, 0)
        grid_layout.addWidget(self.password, 3, 1)

        # Switch
        switch_label = QLabel('Extraction Mode:')
        self.extractionMode = QCheckBox()
        self.extractionMode.setStyleSheet(StyleSheets.switchStyle)
        self.extractionMode.stateChanged.connect(self.onSwitchChange)
        grid_layout.addWidget(switch_label, 4, 0)
        grid_layout.addWidget(self.extractionMode, 4, 1)
        
        # Hide / Extract Button
        self.buttonHideExtract = QPushButton('Hide')
        self.buttonHideExtract.setMinimumWidth(100)
        self.buttonHideExtract.setStyleSheet(StyleSheets.buttonHideExtractStyle)
        self.buttonHideExtract.clicked.connect(lambda: self.runHideExtract())
        grid_layout.addWidget(self.buttonHideExtract, 4, 2)

        # Message box
        self.message_box = QTextEdit()
        self.message_box.setReadOnly(True)
        self.message_box.setMaximumHeight(60)
        self.message_box.setStyleSheet(StyleSheets.messageBoxStyle)
        self.message_box.append('Hiding mode selected.')
        grid_layout.addWidget(self.message_box, 5, 0, 1, 3)
        
    def clearFields(self):
        """
        Clears all input fields.

        Parameters:
        None

        Returns:
        None
        """
        self.inputImagePath.clear()
        self.hiddenFilePath.clear()
        self.outputImagePath.clear()
        self.password.clear()
    
    def showHelpContent(self):
        """
        Displays the help content for the application.
        
        Parameters:
        None

        Returns:
        None
        """
        help_message = \
        (
            "Hide:\n"
            "1. Select an input image file.\n"
            "2. Select a file to hide.\n"
            "3. Select an output image file path and create a name for it.\n"
            "4. Optionally, enter a password to secure the hidden data.\n"
            "5. Click 'Hide' to hide the file within the image.\n\n"
            "Extract:\n"
            "1. Switch to 'Extraction Mode' and select an image with hidden data.\n"
            "4. Enter the password if the image is protected by it.\n"
            "2. Click 'Extract' to retrieve the hidden data."
        )
        self.showCustomDialog("Help Content", help_message)

    def showAbout(self):
        """
        Displays information about the application.
        
        Parameters:
        None

        Returns:
        None
        """
        about_message = \
        (
            "Steganography App v1.0\n"
            "Developed by Marcin Brzozka.\n\n"
            "This application allows you to hide files within images"
            "and extract hidden files from images using steganography."
        )
        self.showCustomDialog("About", about_message)

    def showCustomDialog(self, title, message):
        """
        Displays a custom dialog with a specified title and message.
        
        Parameters:
        title (str): The title of the dialog.
        message (str): The message to display in the dialog.

        Returns:
        None
        """
        dialog = CustomDialog(title, message, self)
        dialog.exec_()
        
    def openFileDialog(self, line_edit, dialog_type):
        """
        Opens a file dialog window and sets the selected file path.
        
        Parameters:
        line_edit (QLineEdit): The line edit widget where the selected file path will be set.
        dialog_type (str): The type of dialog window to open. 
                           It can be 'file' for opening a file or 'save' for saving a file.

        Returns:
        None
        """
        options = QFileDialog.Options()
        if dialog_type == 'file':
            file_name, _ = QFileDialog.getOpenFileName(self, 'Choose File', '', 'All Files (*)', options=options)
            if file_name:
                line_edit.setText(file_name)
        elif dialog_type == 'save':
            file_name, _ = QFileDialog.getSaveFileName(self, 'Save File', '', 'PNG Files (*.png);;All Files (*)', options=options)
            if file_name:
                line_edit.setText(file_name)
            
    def runHideExtract(self):
        """
        Runs the hiding or extraction process based on the selected mode.
        
        Parameters:
        None

        Returns:
        None
        """
        self.message_box.clear()
        if self.extractionMode.isChecked():
            self.extractData()
        else:
            self.hideData()

    def hideData(self):
        """
        Hides data within an image file.
        
        Parameters:
        None

        Returns:
        None
        """
        input_image_path = self.inputImagePath.text()
        hidden_file_path = self.hiddenFilePath.text()
        output_image_path = self.outputImagePath.text()
        password = self.password.text()

        if not (input_image_path and hidden_file_path and output_image_path):
            self.message_box.append('Please fill all required fields.')
            return
        
        try:
            hideDataToImage(input_image_path, hidden_file_path, output_image_path, password)
        except (SystemExit, Exception):
            self.message_box.append('Data not hidden.')
            self.message_box.append('File size too large to hide.')
            return
        
        self.message_box.append('Data hidden successfully.')

    def extractData(self):
        """
        Extracts hidden data from an image file.
        
        Parameters:
        None

        Returns:
        None
        """
        input_image_path = self.inputImagePath.text()
        password = self.password.text()

        if not input_image_path:
            self.message_box.append('Please select an input image.')
            return
        
        try:
            extractDataFromImage(input_image_path, password)
        except (SystemExit, Exception):
            self.message_box.append('Data not extracted.')
            self.message_box.append('Image has no hidden file or wrong password is given.')
            return
        
        self.message_box.append('Data extracted successfully.')

    def onSwitchChange(self, state):
        """
        Handles the change of state in the extraction mode switch.
        
        Parameters:
        state (int): The state of the extraction mode switch (0 for unchecked, 1 for checked).

        Returns:
        None
        """
        self.message_box.clear()
        if state == 0:
            self.message_box.append('Hiding mode selected.')
            self.buttonHideExtract.setText('Hide')
            self.hidden_file_label.setStyleSheet("color: black;")
            self.hiddenFilePath.setEnabled(True)
            self.hiddenFilePath.setStyleSheet(StyleSheets.pathFieldStyle)
            self.hidden_file_button.setEnabled(True)
            self.hidden_file_button.setStyleSheet(StyleSheets.buttonChooseFileStyle)
            self.output_image_label.setStyleSheet("color: black;")
            self.outputImagePath.setEnabled(True)
            self.outputImagePath.setStyleSheet(StyleSheets.pathFieldStyle)
            self.output_image_button.setEnabled(True)
            self.output_image_button.setStyleSheet(StyleSheets.buttonChooseFileStyle)
        else:
            self.message_box.append('Extraction mode selected.')
            self.buttonHideExtract.setText('Extract')
            self.hidden_file_label.setStyleSheet("color: #ABABAB;")
            self.hiddenFilePath.setEnabled(False)
            self.hiddenFilePath.setStyleSheet(StyleSheets.pathFieldOffStyle)
            self.hiddenFilePath.clear()
            self.hidden_file_button.setEnabled(False)
            self.hidden_file_button.setStyleSheet(StyleSheets.buttonChooseFileOffStyle)
            self.output_image_label.setStyleSheet("color: #ABABAB;")
            self.outputImagePath.setEnabled(False)
            self.outputImagePath.setStyleSheet(StyleSheets.pathFieldOffStyle)
            self.outputImagePath.clear()
            self.output_image_button.setEnabled(False)
            self.output_image_button.setStyleSheet(StyleSheets.buttonChooseFileOffStyle)

    def centerWindow(self):
        """
        Centers the main window on the screen.
        This method calculates the position of the window based on the screen size and moves it to the center.

        
        Parameters:
        None

        Returns:
        None
        """
        screen = QDesktopWidget().screenGeometry()
        window_rect = self.geometry()
        x = (screen.width() - window_rect.width()) // 2
        y = (screen.height() - window_rect.height()) // 2
        self.move(x, y)


def main():
    """
    Initializes and runs the main application.
    
    Parameters:
    None

    Returns:
    None
    """
    sys.stdout = open(os.devnull, 'w')
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
