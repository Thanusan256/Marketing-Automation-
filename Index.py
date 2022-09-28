import threading
from time import sleep, time
from xmlrpc.client import Boolean
from PyQt5.QtWidgets import QApplication, QMainWindow
from instagram_private_api import Client as AppClient
import csv
from os import system, name
import webbrowser
from PyQt5 import QtGui
import sys
import os
import requests
from UI import Ui_MainWindow
from Facebook import FacebookGroupPosterGUI
from Instagram import InstagramEmailScraperGUI



def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class MAINCLASSFORUI:
    def __init__(self) -> None:
        self.main_win = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main_win)
        self.ui.homBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.home))
        self.ui.homBtn_2.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.home))
        self.ui.infoBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.info))
        self.ui.infoBtn_2.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.info))
        self.ui.exitBtn.clicked.connect(self.close)
        self.ui.exitBtn_2.clicked.connect(self.close)
        self.ui.facebookAutomationButton.clicked.connect(self.startFB)
        self.ui.emailFetcherButton.clicked.connect(self.startINSTA)
        

    def show(self):
        self.main_win.show()

    def close(self):
        self.main_win.close()

    def startFB(self):
        fb_win = FacebookGroupPosterGUI()
        fb_win.show()

    def startINSTA(self):
        insta_win = InstagramEmailScraperGUI()
        insta_win.show()




        

def start():
    app = QApplication(sys.argv)
    app.setApplicationName("Marketing Software")
    app.setApplicationDisplayName("Marketing Software")
    app.setDesktopFileName("Marketing Software")
    app.setWindowIcon(QtGui.QIcon(resource_path('Blue Creative Lettering Logo.png')))
    main_win = MAINCLASSFORUI()
    main_win.show()
    sys.exit(app.exec_())

start()



