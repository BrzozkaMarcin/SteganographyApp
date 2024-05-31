menuBarStyle = \
"""
    QMenuBar {
        background-color: #E0E0E0;
        border-bottom: 2px solid #C0C0C0;
        color: black;
    }
    QMenuBar::item {
        background-color: transparent;
        padding: 5px 10px;
        border-radius: 5px;
    }
    QMenuBar::item:selected {
        background-color: #A0A0A0;
    }
    QMenu {
        background-color: #E0E0E0;
        border: 2px solid #C0C0C0;
        padding: 5px;
        border-radius: 5px;
    }
    QMenu::item {
        background-color: transparent;
        padding: 5px 20px;
    }
    QMenu::item:selected {
        background-color: #A0A0A0;
    }
"""

dialogStyle = \
"""
    QDialog {
        background-color: #E0E0E0;
        border: 2px solid #E0E0E0;
        border-radius: 10px;
    }
    QLabel {
        color: black;
        font-size: 14px;
        padding: 10px;
    }
    QPushButton {
        background-color: #C0C0C0;
        color: black;
        border-radius: 5px;
        padding: 5px;
    }
    QPushButton:hover {
        background-color: #E0E0E0;
    }
    QPushButton:pressed {
        background-color: #A0A0A0;
    }
"""

pathFieldStyle = \
"""
    background-color: #FFFFFF;
    border: 2px solid #C0C0C0;
    border-radius: 5px;
"""

pathFieldOffStyle = \
"""
    background-color: #DEDEDE;
    border: 2px solid #DEDEDE;
    border-radius: 5px;
"""

buttonChooseFileStyle = \
"""
            QPushButton {
                background-color: #C0C0C0; 
                color: black;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #E0E0E0;
            }
            QPushButton:pressed {
                background-color: #A0A0A0;
            }
"""

buttonChooseFileOffStyle = \
"""
            QPushButton {
                background-color: #DEDEDE; 
                color: #ABABAB;
                border-radius: 5px;
                padding: 5px;
            }
"""

buttonHideExtractStyle = \
"""
            QPushButton {
                background-color: #404040; 
                color: white;
                font-weight: bold;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #606060;
            }
            QPushButton:pressed {
                background-color: #303030;
            }
"""

switchStyle = \
"""
            QCheckBox {
                color: black;
                font-weight: bold;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
            }
            QCheckBox::indicator:unchecked {
                background-color: #C0C0C0;
                border: 2px solid #C0C0C0;
                border-radius: 3px;
            }
            QCheckBox::indicator:unchecked:hover {
                background-color: #E0E0E0;
            }
            QCheckBox::indicator:unchecked:pressed {
                background-color: #A0A0A0;
            }
            QCheckBox::indicator:checked {
                background-color: #404040;
                border: 2px solid #404040;
                border-radius: 3px;
            }
            QCheckBox::indicator:checked:hover {
                background-color: #606060;
            }
            QCheckBox::indicator:checked:pressed {
                background-color: #303030;
            }
"""

messageBoxStyle = \
"""
    QTextEdit {
        background-color: #FFFFFF;
        border: 2px solid #C0C0C0;
        border-radius: 5px;
        padding: 5px;
    }
"""
