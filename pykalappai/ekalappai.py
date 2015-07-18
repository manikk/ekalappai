__author__ = 'manikk'

import sys
import time
import os
import shutil

import ekalappai_rc

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.Qt import QSharedMemory, QSplashScreen, \
    QSystemTrayIcon, qApp, QSettings, QGroupBox, QLabel, \
    QComboBox, QIcon, QHBoxLayout,QCheckBox,QAction,QDialog,QMenu,QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import qWarning

class EKWindow(QDialog):

    def createSettingsGroupBoxes(self):
        self.iconGroupBox = QGroupBox("Keyboards")
        self.iconLabel = QLabel("Keyboard:")
        self.iconComboBox = QComboBox(self)
        self.iconComboBox.addItem(QIcon(":/images/ekalappai_icons_en.png"), "No Keyboard")
        self.iconComboBox.addItem(QIcon(":/images/ekalappai_icons_tn99.png"), "Tamil99")
        self.iconComboBox.addItem(QIcon(":/images/ekalappai_icons_anjal.png"), "Phonetic")
        self.iconComboBox.addItem(QIcon(":/images/ekalappai_icons_tw.png"), "Typewriter")
        self.iconComboBox.addItem(QIcon(":/images/ekalappai_icons_bamini.png"), "Bamini")
        self.iconComboBox.addItem(QIcon(":/images/ekalappai_icons_inscript.png"), "Inscript")

        iconLayout = QHBoxLayout(self)
        iconLayout.addWidget(self.iconLabel)
        iconLayout.addWidget(self.iconComboBox)
        iconLayout.addStretch()
        self.iconGroupBox.setLayout(iconLayout)

        self.shortcutGroupBox = QGroupBox("Shortcut Setting")
        shortcutLabel1 = QLabel("Modifier Key:")
        shortcutLabel2 = QLabel("Shortcut Key:")

        self.shortcutComboBox1 = QComboBox(self)
        self.shortcutComboBox1.addItem("NONE")
        self.shortcutComboBox1.addItem("CTRL")
        self.shortcutComboBox1.addItem("ALT")

        indexTmp1 = self.shortcutComboBox1.findText(self.shortCutModifierKey)
        self.shortcutComboBox1.setCurrentIndex(indexTmp1)

        self.shortcutComboBox2 = QComboBox(self)
        self.shortcutComboBox2.setMinimumContentsLength(3)

        if indexTmp1 == 0:
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


        indexTmp2 = self.shortcutComboBox2.findText(self.shortcutKey)
        self.shortcutComboBox2.setCurrentIndex(indexTmp2)

        shortcutLayout = QHBoxLayout(self)
        shortcutLayout.addWidget(shortcutLabel1)
        shortcutLayout.addWidget(self.shortcutComboBox1)
        shortcutLayout.addWidget(shortcutLabel2)
        shortcutLayout.addWidget(self.shortcutComboBox2)
        shortcutLayout.addStretch()
        self.shortcutGroupBox.setLayout(shortcutLayout)

        self.otherSettingsGroupBox = QGroupBox("Other Settings");

        checkboxStartWithWindowsLabel = QLabel("Start eKalappai whenever windows starts")
        self.checkboxStartWithWindows = QCheckBox()

        #if registry entry for auto start with windows for the current user exists, then check the checkbox
        if self.registrySettings.contains(qApp.applicationName()):
             self.checkboxStartWithWindows.setChecked(True)
        else:
             self.checkboxStartWithWindows.setChecked(False)

        otherSettingsLayout = QHBoxLayout(self)
        otherSettingsLayout.addWidget(checkboxStartWithWindowsLabel)
        otherSettingsLayout.addWidget(self.checkboxStartWithWindows)
        otherSettingsLayout.addStretch()
        self.otherSettingsGroupBox.setLayout(otherSettingsLayout)

    #This function is called when the shortcut combo is changed
    def setShortcut2(self, index) :
        self.shortcutKey =   self.shortcutComboBox2.currentText()
        self.iniSettings.setValue("shortcut", self.shortcutKey)
        if self.shortcutKey == "ESC" :
            self.shortCutKeyHex = 0x1B
        elif self.shortcutKey == "F1" :
            self.shortCutKeyHex = 0x70
        elif self.shortcutKey == "F2":
            self.shortCutKeyHex = 0x71
        elif self.shortcutKey == "F3":
            self.shortCutKeyHex = 0x72
        elif self.shortcutKey == "F4":
            self.shortCutKeyHex = 0x73
        elif self.shortcutKey == "F5":
            self.shortCutKeyHex = 0x74
        elif self.shortcutKey == "F6":
            self.shortCutKeyHex = 0x75
        elif self.shortcutKey == "F7":
            self.shortCutKeyHex = 0x76
        elif self.shortcutKey == "F8":
            self.shortCutKeyHex = 0x77
        elif self.shortcutKey == "F9":
            self.shortCutKeyHex = 0x78
        elif self.shortcutKey == "F10":
            self.shortCutKeyHex = 0x79
        elif self.shortcutKey == "1":
            self.shortCutKeyHex = 0x31
        elif self.shortcutKey == "2":
            self.shortCutKeyHex = 0x32
        elif self.shortcutKey == "3":
            self.shortCutKeyHex = 0x33
        elif self.shortcutKey == "4":
            self.shortCutKeyHex = 0x34
        elif self.shortcutKey == "5":
            self.shortCutKeyHex = 0x35
        elif self.shortcutKey == "6":
            self.shortCutKeyHex = 0x36
        elif self.shortcutKey == "7":
            self.shortCutKeyHex = 0x37
        elif self.shortcutKey == "8":
            self.shortCutKeyHex = 0x38
        elif self.shortcutKey == "9":
            self.shortCutKeyHex = 0x39
        elif self.shortcutKey == "0":
            self.shortCutKeyHex = 0x30

    def createActions(self):
        self.minimizeAction = QAction("Mi&nimize", self)
        self.minimizeAction.triggered.connect(self.hide)

        self.maximizeAction = QAction("Ma&ximize", self)
        self.maximizeAction.triggered.connect(self.showMaximized)

        self.settingsAction = QAction("&Settings", self);
        self.settingsAction.triggered.connect(self.showNormal)

        self.aboutAction = QAction("&About",self);
        self.aboutAction.triggered.connect(self.showAbout)

        self.quitAction = QAction("&Quit", self);
        self.quitAction.triggered.connect(qApp.quit)

    def createTrayIcon(self):
        self.trayIconMenu = QMenu(self)
        self.trayIconMenu.addAction(self.settingsAction)
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addAction(self.aboutAction)
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addAction(self.quitAction)

        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setContextMenu(self.trayIconMenu)

    def setVisible(self,visible):
        self.settingsAction.setEnabled(self.isMaximized() or not visible)
        super(EKWindow, self).setVisible(visible)

    def closeEvent(self, event) :
        if self.trayIcon.isVisible():
            self.hide()
            event.ignore()

    def loadKeyBoard(self):
        #file handling code
        if self.selectedKeyboard == 1 :
            self.fileName = "keyboards/Tamil-tamil99.txt.in"
        elif self.selectedKeyboard == 2 :
            self.fileName = "keyboards/Tamil-phonetic.txt.in"
        elif self.selectedKeyboard == 3 :
            self.fileName = "keyboards/Tamil-typewriter.txt.in"
        elif self.selectedKeyboard == 4 :
            self.fileName = "keyboards/Tamil-bamini.txt.in"
        elif self.selectedKeyboard == 5:
            self.fileName = "keyboards/Tamil-inscript.txt.in"
        else:
            pass

    #This function is called when keyboard is toggled or when keyboard is changed from setting window.
    def changeKeyboard(self,index):
        icon = self.iconComboBox.itemIcon(index)
        self.trayIcon.setIcon(icon)
        self.setWindowIcon(icon)
        self.trayIcon.setToolTip(self.iconComboBox.itemText(index));
        #call remove hook before cecking for the keyboard choosen .
        #removeHook();
        #logic to start a keyboard hook or remove keyboard hook based on the keyboard choosen
        #callHook(index);
        self.showTrayMessage(index)
        self.loadKeyBoard()

    #This functions is called when taskbar icon is clicked
    def iconActivated(self, reason) :
        if reason == QSystemTrayIcon.DoubleClick:
            pass
        elif reason == QSystemTrayIcon.Trigger:
            if self.keyboardStatus:
                self.keyboardStatus = False
            else:
                self.keyboardStatus = True

            if self.keyboardStatus:
                 if self.currentKeyboard == 0:
                    self.changeKeyboard(self.selectedKeyboar)
            else:
                if self.currentKeyboard > 0:
                     self.changeKeyboard(0)
        elif reason == QSystemTrayIcon.MiddleClick:
            pass
        else:
            pass

    def showTrayMessage(self, index):
        icon = QSystemTrayIcon.MessageIcon(0)
        #this system messages proves to be more annoyance than benefit so hiding it
        message = self.iconComboBox.itemText(index)+ " set";
        self.trayIcon.showMessage(qApp.applicationName() + " " + qApp.applicationVersion(),message, icon, 100)

    #Function to add or disable registry entry to auto start ekalappai with windows for the current users
    def checkboxStartWithWindowsTicked(self):
        if self.checkboxStartWithWindows.isChecked():
            self.registrySettings.setValue(qApp.applicationName(),qApp.applicationFilePath())
            #registry_settings->setValue(qApp->applicationName(),QDir::toNativeSeparators(qApp->applicationFilePath()));
        else :
            self.registrySettings.remove(qApp.applicationName())

    def showAbout(self):
        pass

    #This function is called when the shortcut modifier combo is changed
    def setShortcut1(self,index):
        self.iniSettings.setValue("shortcut_modifier", self.shortcutComboBox1.currentText())
        self.shortcutModifierKey = self.initSettings.value("shortcut_modifier")
        #if none is selected, the allowed single key shortcuts should change
        if index == 0 :
            self.shortcutComboBox2.clear()
            self.shortcutComboBox2.addItem("ESC");
            self.shortcutComboBox2.addItem("F1");
            self.shortcutComboBox2.addItem("F2");
            self.shortcutComboBox2.addItem("F3");
            self.shortcutComboBox2.addItem("F4");
            self.shortcutComboBox2.addItem("F5");
            self.shortcutComboBox2.addItem("F6");
            self.shortcutComboBox2.addItem("F7");
            self.shortcutComboBox2.addItem("F8");
            self.shortcutComboBox2.addItem("F9");
            self.shortcutComboBox2.addItem("F10");
        else :
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

    def __init__(self):
        super(EKWindow, self).__init__()
        settingsFilePath = os.getenv("APPDATA") + "\\" + qApp.applicationName() + "\eksettings.ini"
        if not os.path.exists(settingsFilePath):
            shutil.copyfile(qApp.applicationDirPath() + "\eksettings.ini", settingsFilePath)
            pass

        self.keyboardStatus = False
        self.iniSettings = QSettings(settingsFilePath, QSettings.IniFormat)
        self.registrySettings = QSettings("HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run", QSettings.NativeFormat);
        self.shortCutModifierKey = self.iniSettings.value("shortcut_modifier")
        self.shortcutKey = self.iniSettings.value("shortcut")
        self.selectedKeyboard = self.iniSettings.value("selected_keyboard")

        self.createSettingsGroupBoxes()
        self.setShortcut2(0)
        self.createActions()
        self.createTrayIcon()

        self.iconComboBox.currentIndexChanged.connect(self.changeKeyboard)
        self.shortcutComboBox1.currentIndexChanged.connect(self.setShortcut1)
        self.shortcutComboBox2.currentIndexChanged.connect(self.setShortcut2)
        self.trayIcon.activated.connect(self.iconActivated)

        #self.checkboxStartWithWindows.stateChanged.connect(self.checkboxStartWithWindowsTicked)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.iconGroupBox)
        self.mainLayout.addWidget(self.shortcutGroupBox)
        self.mainLayout.addWidget(self.otherSettingsGroupBox)
        self.setLayout(self.mainLayout);

        if self.keyboardStatus == True :
            self.iconComboBox.setCurrentIndex(self.selectedKeyBoard);
        else :
            self.changeKeyboard(0);
            self.iconComboBox.setCurrentIndex(0);

        self.trayIcon.show()

        self.setWindowTitle(qApp.applicationName()+ " " + qApp.applicationVersion())


if __name__ == '__main__' :
    print("called")
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
    # if not QSystemTrayIcon.isSystemTrayAvailable():

    QApplication.setQuitOnLastWindowClosed(False)
    ekWindow = EKWindow()

    sys.exit(app.exec_())








