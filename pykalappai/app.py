__author__ = "Manikk, Vijay, Mohan"
__copyright__ = "Copyright (c) 2015 http://thamizha.com/"
__credits__ = ["Manikk, Vijay, Mohan"]
__license__ = "GNU/GPL v3 or (at your option) any later version."
__version__ = "4.0.0"
__maintainer__ = "http://thamizha.com/"
__email__ = ""
__status__ = "Development"

import os
import shutil
import time
import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.Qt import QSharedMemory, QSplashScreen, \
    QSystemTrayIcon, qApp, QSettings, QGroupBox, QLabel, \
    QComboBox, QIcon, QHBoxLayout, QCheckBox, QAction, QDialog, QMenu, QVBoxLayout
from PyQt5.QtCore import qWarning
from PyQt5.QtGui import QPixmap

from resources import ekalappai_rc
from EkEngine import Engine


class EKWindow(QDialog):
    """
        Class which is responisble for running this entire application
    """

    def __init__(self):
        """
            Constructor for this class
        """
        super(EKWindow, self).__init__()
        self.engine = Engine("tables/Tamil-bamini.txt.in")

        # Settings file initialization
        self.settingsFilePath = os.getenv("APPDATA") + "\\" + qApp.applicationName() + "\eksettings.ini"
        self.init_settings()    # Function to check whether the settings file is or not.
        self.iniSettings = QSettings(self.settingsFilePath, QSettings.IniFormat)

        # Variable Initialization
        self.registrySettings = QSettings("HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run", QSettings.NativeFormat)
        self.shortcutModifierKey = self.iniSettings.value("shortcut_modifier")
        self.shortcutKey = self.iniSettings.value("shortcut")
        self.selectedKeyboard = self.iniSettings.value("selected_keyboard")
        self.keyboardStatus = False
        self.fileName = ""

        # Ui variable Initialization
        self.iconGroupBox = QGroupBox("Keyboards")
        self.iconLabel = QLabel("Keyboard:")
        self.iconComboBox = QComboBox(self)
        self.shortcutGroupBox = QGroupBox("Shortcut Setting")
        self.shortcutComboBox1 = QComboBox(self)
        self.shortcutComboBox2 = QComboBox(self)
        self.otherSettingsGroupBox = QGroupBox("Other Settings")
        self.checkboxStartWithWindows = QCheckBox()
        self.minimizeAction = QAction("Minimize", self)
        self.maximizeAction = QAction("Maximize", self)
        self.settingsAction = QAction("Settings", self)
        self.aboutAction = QAction("About", self)
        self.quitAction = QAction("Quit", self)
        self.trayIconMenu = QMenu(self)
        self.trayIcon = QSystemTrayIcon(self)
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.iconGroupBox)
        self.mainLayout.addWidget(self.shortcutGroupBox)
        self.mainLayout.addWidget(self.otherSettingsGroupBox)
        self.setLayout(self.mainLayout)

        # UI constructor and connectors
        self.create_settings_group_boxes()
        self.create_actions()
        self.create_tray_icon()

        # Signal connectors
        self.iconComboBox.currentIndexChanged.connect(self.change_keyboard)
        self.shortcutComboBox1.currentIndexChanged.connect(self.set_shortcut_modifier)
        self.shortcutComboBox2.currentIndexChanged.connect(self.set_shortcut_key)
        self.trayIcon.activated.connect(self.icon_activated)
        self.checkboxStartWithWindows.stateChanged.connect(self.checkbox_start_with_windows_ticked)

        if self.keyboardStatus:
            self.iconComboBox.setCurrentIndex(self.selectedKeyBoard)
        else:
            self.change_keyboard(0)
            self.iconComboBox.setCurrentIndex(0)

        self.trayIcon.show()
        self.set_shortcut_key()
        self.setWindowTitle(qApp.applicationName() + " " + qApp.applicationVersion())

    def init_settings(self):
        """
            Function to check whether the settings file is there or not. If there is no file, then it will create with
            default settings.
        """
        if not os.path.exists(self.settingsFilePath):
            settings_dir = os.getenv("APPDATA") + "\\" + qApp.applicationName()
            if not os.path.exists(settings_dir):
                os.makedirs(settings_dir)
            setting_path = ""
            if getattr(sys, 'frozen', False):
                setting_path = os.path.dirname(sys.executable)
            elif __file__:
                setting_path = os.path.dirname(__file__)
            shutil.copyfile(os.path.join(setting_path, "resources\eksettings.ini"), self.settingsFilePath)
        return

    def create_settings_group_boxes(self):
        """
            UI generator function.
        """
        self.iconComboBox.addItem("No Keyboard")
        self.iconComboBox.addItem("Tamil99")
        self.iconComboBox.addItem("Phonetic")
        self.iconComboBox.addItem("Typewriter")
        self.iconComboBox.addItem("Bamini")
        self.iconComboBox.addItem("Inscript")
        icon_layout = QHBoxLayout(self)
        icon_layout.addWidget(self.iconLabel)
        icon_layout.addWidget(self.iconComboBox)
        icon_layout.addStretch()
        self.iconGroupBox.setLayout(icon_layout)

        shortcut_label_1 = QLabel("Modifier Key:")
        shortcut_label_2 = QLabel("Shortcut Key:")

        self.shortcutComboBox1.addItem("NONE")
        self.shortcutComboBox1.addItem("CTRL")
        self.shortcutComboBox1.addItem("ALT")

        modifier_index = self.shortcutComboBox1.findText(self.shortcutModifierKey)
        self.shortcutComboBox1.setCurrentIndex(modifier_index)

        self.shortcutComboBox2.setMinimumContentsLength(3)

        if modifier_index == 0:
            self.shortcutComboBox2.addItem("F1")
            self.shortcutComboBox2.addItem("ESC")
            self.shortcutComboBox2.addItem("F2")
            self.shortcutComboBox2.addItem("F3")
            self.shortcutComboBox2.addItem("F4")
            self.shortcutComboBox2.addItem("F5")
            self.shortcutComboBox2.addItem("F6")
            self.shortcutComboBox2.addItem("F7")
            self.shortcutComboBox2.addItem("F8")
            self.shortcutComboBox2.addItem("F9")
            self.shortcutComboBox2.addItem("F10")
        else:
            self.shortcutComboBox2.addItem("1")
            self.shortcutComboBox2.addItem("2")
            self.shortcutComboBox2.addItem("3")
            self.shortcutComboBox2.addItem("4")
            self.shortcutComboBox2.addItem("5")
            self.shortcutComboBox2.addItem("6")
            self.shortcutComboBox2.addItem("7")
            self.shortcutComboBox2.addItem("8")
            self.shortcutComboBox2.addItem("9")
            self.shortcutComboBox2.addItem("0")

        key_index = self.shortcutComboBox2.findText(self.shortcutKey)
        self.shortcutComboBox2.setCurrentIndex(key_index)

        shortcut_layout = QHBoxLayout(self)
        shortcut_layout.addWidget(shortcut_label_1)
        shortcut_layout.addWidget(self.shortcutComboBox1)
        shortcut_layout.addWidget(shortcut_label_2)
        shortcut_layout.addWidget(self.shortcutComboBox2)
        shortcut_layout.addStretch()
        self.shortcutGroupBox.setLayout(shortcut_layout)

        checkbox_start_with_windows_label = QLabel("Start eKalappai whenever windows starts")

        # if registry entry for auto start with windows for the current user exists, then check the checkbox
        if self.registrySettings.contains(qApp.applicationName()):
            self.checkboxStartWithWindows.setChecked(True)
        else:
            self.checkboxStartWithWindows.setChecked(False)

        other_settings_layout = QHBoxLayout(self)
        other_settings_layout.addWidget(checkbox_start_with_windows_label)
        other_settings_layout.addWidget(self.checkboxStartWithWindows)
        other_settings_layout.addStretch()
        self.otherSettingsGroupBox.setLayout(other_settings_layout)

    def set_shortcut_key(self):
        """
            Function to change the shortcut key when its changed.
        """
        self.shortcutKey = self.shortcutComboBox2.currentText()
        self.iniSettings.setValue("shortcut", self.shortcutKey)
        self.register_shortcut_listener()
        if self.shortcutKey == "ESC":
            self.shortcutKeyHex = 0x1B
        elif self.shortcutKey == "F1":
            self.shortcutKeyHex = 0x70
        elif self.shortcutKey == "F2":
            self.shortcutKeyHex = 0x71
        elif self.shortcutKey == "F3":
            self.shortcutKeyHex = 0x72
        elif self.shortcutKey == "F4":
            self.shortcutKeyHex = 0x73
        elif self.shortcutKey == "F5":
            self.shortcutKeyHex = 0x74
        elif self.shortcutKey == "F6":
            self.shortcutKeyHex = 0x75
        elif self.shortcutKey == "F7":
            self.shortcutKeyHex = 0x76
        elif self.shortcutKey == "F8":
            self.shortcutKeyHex = 0x77
        elif self.shortcutKey == "F9":
            self.shortcutKeyHex = 0x78
        elif self.shortcutKey == "F10":
            self.shortcutKeyHex = 0x79
        elif self.shortcutKey == "1":
            self.shortcutKeyHex = 0x31
        elif self.shortcutKey == "2":
            self.shortcutKeyHex = 0x32
        elif self.shortcutKey == "3":
            self.shortcutKeyHex = 0x33
        elif self.shortcutKey == "4":
            self.shortcutKeyHex = 0x34
        elif self.shortcutKey == "5":
            self.shortcutKeyHex = 0x35
        elif self.shortcutKey == "6":
            self.shortcutKeyHex = 0x36
        elif self.shortcutKey == "7":
            self.shortcutKeyHex = 0x37
        elif self.shortcutKey == "8":
            self.shortcutKeyHex = 0x38
        elif self.shortcutKey == "9":
            self.shortcutKeyHex = 0x39
        elif self.shortcutKey == "0":
            self.shortcutKeyHex = 0x30

    def create_actions(self):
        """
            Slot connectors for all right clicking and other actions.
        """
        self.minimizeAction.triggered.connect(self.hide)
        self.maximizeAction.triggered.connect(self.showMaximized)
        self.settingsAction.triggered.connect(self.showNormal)
        self.aboutAction.triggered.connect(self.show_about)
        self.quitAction.triggered.connect(self.quit)

    def quit(self):
        self.engine.un_hook()
        exit(0)

    def create_tray_icon(self):
        """
            Tray icon creator and corresponding connectors
        """
        self.trayIconMenu.addAction(self.settingsAction)
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addAction(self.aboutAction)
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addAction(self.quitAction)
        self.trayIcon.setContextMenu(self.trayIconMenu)

    def setVisible(self, visible):
        self.settingsAction.setEnabled(self.isMaximized() or not visible)
        super(EKWindow, self).setVisible(visible)

    def closeEvent(self, event):
        if self.trayIcon.isVisible():
            self.hide()
            event.ignore()

    def load_keyboard(self):
        """
            Mapping file loading function
        """
        if self.selectedKeyboard == 1:
            self.fileName = "tables/Tamil-tamil99.txt.in"
        elif self.selectedKeyboard == 2:
            self.fileName = "tables/Tamil-phonetic.txt.in"
        elif self.selectedKeyboard == 3:
            self.fileName = "tables/Tamil-typewriter.txt.in"
        elif self.selectedKeyboard == 4:
            self.fileName = "tables/Tamil-bamini.txt.in"
        elif self.selectedKeyboard == 5:
            self.fileName = "tables/Tamil-inscript.txt.in"
        else:
            pass

    def getPath(self, index):
            if index == 1:
                self.path = "tables/Tamil-tamil99.txt.in"
            elif index == 2:
                self.path = "tables/Tamil-phonetic.txt.in"
            elif index == 3:
                self.path = "tables/Tamil-typewriter.txt.in"
            elif index == 4:
                self.path = "tables/Tamil-bamini.txt.in"
            elif index == 5:
                self.path = "tables/Tamil-inscript.txt.in"
            else:
                pass

    def change_keyboard(self, index):
        """
            Function to change the keyboard based on the index which was sent as a param
        """
        if int(index) != 0:
            self.iniSettings.setValue("selected_keyboard", index)
            self.selectedKeyboard = index
        self.iconComboBox.setCurrentIndex(int(index))
        icon = self.iconComboBox.itemIcon(int(index))
        self.trayIcon.setIcon(icon)
        self.setWindowIcon(icon)
        self.trayIcon.setToolTip(self.iconComboBox.itemText(int(index)))
        self.show_tray_message(index)
        self.load_keyboard()
        if int(index) != 0:
            self.getPath(int(index))
            self.engine.file_name = self.path
            self.engine.initialize()
            self.engine.conv_state = True
        else:
            try:
                self.engine.conv_state = False
            except:
                pass

    def icon_activated(self, reason):
        """
            Function to toggle the state when the icon is clicked or shortcut key is pressed
        """
        if reason == QSystemTrayIcon.DoubleClick:
            pass
        elif reason == QSystemTrayIcon.Trigger:
            if self.keyboardStatus:
                self.keyboardStatus = False
            else:
                self.keyboardStatus = True
            if self.keyboardStatus:
                self.change_keyboard(self.selectedKeyboard)
            else:
                self.change_keyboard(0)
        elif reason == QSystemTrayIcon.MiddleClick:
            pass
        else:
            pass

    def show_tray_message(self, index):
        """
            Tray message generator when there is change in keyboard state
        """
        icon = QSystemTrayIcon.MessageIcon(0)
        message = self.iconComboBox.itemText(int(index)) + " set"
        self.trayIcon.showMessage(qApp.applicationName() + " " + qApp.applicationVersion(), message, icon, 100)

    def checkbox_start_with_windows_ticked(self):
        """
            Function to add or disable registry entry to auto start ekalappai with windows for the current users
        """
        if self.checkboxStartWithWindows.isChecked():
            self.registrySettings.setValue(qApp.applicationName(), qApp.applicationFilePath())
        else:
            self.registrySettings.remove(qApp.applicationName())

    def show_about(self):
        pass

    def set_shortcut_modifier(self, index):
        """
            Function to set the shortcut modifier when its changed.
        """
        self.iniSettings.setValue("shortcut_modifier", self.shortcutComboBox1.currentText())
        self.shortcutModifierKey = self.iniSettings.value("shortcut_modifier")
        # if none is selected, the allowed single key shortcuts should change
        if index == 0:
            self.shortcutComboBox2.clear()
            self.shortcutComboBox2.addItem("ESC")
            self.shortcutComboBox2.addItem("F1")
            self.shortcutComboBox2.addItem("F2")
            self.shortcutComboBox2.addItem("F3")
            self.shortcutComboBox2.addItem("F4")
            self.shortcutComboBox2.addItem("F5")
            self.shortcutComboBox2.addItem("F6")
            self.shortcutComboBox2.addItem("F7")
            self.shortcutComboBox2.addItem("F8")
            self.shortcutComboBox2.addItem("F9")
            self.shortcutComboBox2.addItem("F10")
        else:
            self.shortcutComboBox2.clear()
            self.shortcutComboBox2.addItem("1")
            self.shortcutComboBox2.addItem("2")
            self.shortcutComboBox2.addItem("3")
            self.shortcutComboBox2.addItem("4")
            self.shortcutComboBox2.addItem("5")
            self.shortcutComboBox2.addItem("6")
            self.shortcutComboBox2.addItem("7")
            self.shortcutComboBox2.addItem("8")
            self.shortcutComboBox2.addItem("9")
            self.shortcutComboBox2.addItem("0")
        self.register_shortcut_listener()

    def register_shortcut_listener(self):
        self.engine.event_queue.remove_all()
        if self.iniSettings.value("shortcut_modifier") == "NONE":
            self.engine.event_queue.register_event([[self.shortcutKey], self.icon_activated, QSystemTrayIcon.Trigger])
        elif self.iniSettings.value("shortcut_modifier") == "CTRL":
            self.engine.event_queue.register_event([['Lcontrol', self.shortcutKey], self.icon_activated, QSystemTrayIcon.Trigger])
            self.engine.event_queue.register_event([['Rcontrol', self.shortcutKey], self.icon_activated, QSystemTrayIcon.Trigger])
        elif self.iniSettings.value("shortcut_modifier") == "ALT":
            self.engine.event_queue.register_event([['LMenu', self.shortcutKey], self.icon_activated, QSystemTrayIcon.Trigger])
            self.engine.event_queue.register_event([['RMenu', self.shortcutKey], self.icon_activated, QSystemTrayIcon.Trigger])
        return True


if __name__ == "__main__":
    """
        Main Function which will initialize the app
    """
    app = QApplication(sys.argv)
    app.setApplicationName("eKalappai")
    app.setApplicationVersion("4.0.0")
    shared = QSharedMemory("59698760-43bb-44d9-8121-181ecbb70e4d")

    if not shared.create(512, QSharedMemory.ReadWrite):
        qWarning("Cannot start more than one instance of eKalappai any time.")
        exit(0)
    splashImage = QPixmap(':/images/intro.png')
    splashScreen = QSplashScreen(splashImage)
    splashScreen.show()
    time.sleep(2)
    splashScreen.hide()
    QApplication.setQuitOnLastWindowClosed(False)
    ekWindow = EKWindow()
    ekWindow.engine.start()
    sys.exit(app.exec_())
