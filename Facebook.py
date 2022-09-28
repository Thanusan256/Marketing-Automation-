from pickle import NONE
from re import sub
from tkinter.constants import ANCHOR, FALSE, TRUE, Y
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from tkinter import PhotoImage, filedialog
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
import time
from datetime import date
import webbrowser
import sys
import os
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow
from FacebookUI import Ui_Form
from PyQt5 import QtGui


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


LOGIN_URL = 'https://m.facebook.com/login'

status = None
msgG = None
frame = None
intervalG = None
keywordG = None
maxGrps = None
postToGroups = None


class FaceBookGroupPoster():
    def __init__(self):
        self.groups = []
        self.images = []
        self.videos = []
        self.discussGrp = False
    
    #If you delete "do not delethis", it wont work, even that value is not used.
    def startFaceBookGroupPoster(self, frame, doNotDeleteThis):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        prefs = {"profile.default_content_setting_values.notifications": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        self.driver.get(LOGIN_URL)
        frame.setText("Make sure you are logged in before proceeding")
        frame.setStyleSheet("color: green;")

    def terminate(self):
        self.driver.close()

    def postGroups(self):
        global msgG, frame, intervalG, keywordG, maxGrps, postToGroups

        msg = msgG.toPlainText().encode("utf-8")
        interval =  intervalG.text()
        keyword = keywordG.text()
        maxGrp = int(maxGrps.text())
        frame.setText(f'Ok Executing the program, Please wait patiently, once its done we will update here.')
        try:
            int(interval)
        except ValueError:
            frame.setText("Please enter a number as value as timout")
            frame.setStyleSheet("color: red;")
            return
        try:
            if len(self.groups) <= 0:
                if len(keyword) <= 0:
                    frame.setText("No groups and keyword loaded \n Make sure you load the groups or keyword before continue")
                    frame.setStyleSheet("color: red;")
                    return
                else:
                    try:
                        maxGrpInt = int(maxGrp)
                        self.getJoinedGroups(frame,keyword, maxGrpInt)
                    except ValueError:
                        frame.setText("Please enter a number as maximum groups.")
                        frame.setStyleSheet("color: red;")
                        return
                    
                
            elif len(self.images) == 0 and len(msg) == 0:
                frame.setText("First select images or type a message")
                frame.setStyleSheet("color: red;")
                return
            frame.setText(f' We will be trying to post to total of {len(self.groups)} groups with a interval of {interval} seconds')
            try:
                f = open("logs.txt", "a", encoding="utf-8")
                f.write(
                    f'\n\n\n Logs for {msg} at {date.today()} \n ==========================================================================================\n')
                f.close()
                for group in self.groups:
                    self.driver.get(group)
                    time.sleep(5)
                    print(f'trying to post to {group}')
                    try:
                        print("Checking for group TYPE")
                        discuss = self.driver.find_element_by_css_selector("button[value='Discuss']")
                        self.discussGrp = True
                        print("Group Type: Buy and Sell grp (Try to post as discuss)")
                        discuss.click()
                        time.sleep(3)
                    except Exception as e:
                        print("Group Type: Normal Facebook Group")
                        self.discussGrp = False
 
                    try:
                        if self.discussGrp:
                            postStart = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located(
                            (By.XPATH, '//div[starts-with(text(),"Write something")]')))
                        else:
                            postStart = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                            (By.XPATH, '//div[starts-with(text(),"Write something...")]')))
                    except Exception:
                        try:
                            postStart = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                                (By.XPATH, '//div[starts-with(text(),"Create a public")]')))
                        except Exception:
                            try:
                                postStart = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                                (By.XPATH, '//div[starts-with(text(),"What\'s on your mind")]')))
                            except Exception:
                                try:
                                    postStart = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                                    (By.XPATH, "//textarea[@id='uniqid_1']")))
                                except Exception:
                                    try:
                                        postStart = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                                        (By.TAG_NAME, 'textarea')))
                                    except Exception as e:
                                        print(f'Tried to get the postStart Btn but could not with the error {e}\n Tried "Write Something, Write something..., Create a public post, whats on your mind, unique_id1 and tag name == textarea')

                    time.sleep(1)
                    try:
                        postStart.click()
                    except Exception as e:
                        try:
                            ActionChains(self.driver).move_to_element(
                            postStart).click().perform()
                        except Exception as e:
                            print(f'The create post btn found but could not click, Trying to send text to input box anyway.')
                    try:
                        txtBox = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, "//textarea[last()]")))
                    except Exception:
                        try:
                            txtBox = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(
                            (By.XPATH, "//textarea[@id='uniqid_1']")))
                        except Exception:
                            try:
                                txtBox = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(
                                (By.TAG_NAME, 'textarea')))
                            except Exception as e:
                                print(f'Could not find the txtBox with the error {e}\n Tried "textareal[last()], unique_id1 and tag name == textarea')
                    try:
                        txtBox.send_keys(msg.decode('utf8', 'ignore'))
                        time.sleep(2)
                    except Exception as e:
                        try:
                            ActionChains(self.driver).move_to_element(
                            txtBox).send_keys(msg.decode('utf8', 'ignore')).perform()
                        except Exception as e:
                            print(f'Text box found but could not send texts with error {e}')
                        time.sleep(2)

                    for photo in self.images:
                        try:
                            photo_element = WebDriverWait(self.driver, 5).until(
                                EC.presence_of_element_located((By.XPATH, "//input[@name='file1']")))
                            photo_element.send_keys(photo)
                            time.sleep(2)
                        except Exception as e:
                            print(f'Could not send {photo} with the error {e}')

                    for video in self.videos:
                        try:
                            video_element = WebDriverWait(self.driver, 5).until(
                                EC.presence_of_element_located((By.XPATH, "//input[@name='file2']")))
                            video_element.send_keys(video)
                            time.sleep(2)
                        except Exception as e:
                            print(f'Could not send Video {video} with the error {e}')

                    time.sleep(5)
                    try:
                        time.sleep(2)
                        post = WebDriverWait(self.driver, 5).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='acw'] button[value='Post']")))
                        post.click()
                    except Exception as e:
                        print('Trying to post using the last method. (usually this happens in buy and sell grp). But you can ignore this as long as program executes.')
                        time.sleep(5)
                        try:
                            txtBox = WebDriverWait(self.driver, 5).until(
                            EC.presence_of_element_located((By.XPATH, "//textarea[last()]")))
                            txtBox.submit()
                        except Exception:
                            pass
                    time.sleep(5)
                    f = open("logs.txt", "a")
                    f.write(f'{group} processed.\n ')
                    f.close()
                    print(f'Hey I am waiting for {interval} seconds, as you mentioned')
                    time.sleep(int(interval))
                    time.sleep(2)
            except Exception as e:
                print(f'ERROR OCCURRED: {e}')
                f = open("logs.txt", "a")
                f.write(f'FAILED Posting to {msg}: {e}\n')
                f.close()
        except Exception as e:
            print(f'ERROR OCCURRED: {e}')
            f = open("logs.txt", "a")
            f.write(f'FAILED Posting to {msg}: {e}\n')
            f.close()
            postToGroups.exit()
        print("PROGRAM EXECUTING FINISHED \n =============================================== \n Thanks for using facebook group poster pro.")
        frame.setText("All done, Check the logs.txt file at your current folder")
        frame.setStyleSheet("color: green;")
        self.groups = []

    def getImages(self, frame):
        filenames = filedialog.askopenfilenames(
            initialdir="/", title="Select Image", filetypes=(("JPG", "*.jpg"), ("PNG Files", "*.png"), ("all files", "*.*")))
        for img in filenames:
            self.images.append(img)

        frame.setText(f'{frame.text()}\n{len(self.images)} images loaded')
        frame.setStyleSheet("color: green;")
        

    def addGroups(self, frame):
        filename = filedialog.askopenfilename(
            initialdir="/", title="Select file", filetypes=(("Texts Files", "*.txt"), ("all files", "*.*")))
        print(f'{filename}')
        with open(filename, 'r') as f:
            try:
                tempGroups = f.read()
                tempGroups = tempGroups.split(',')
                tempAllGroups = [x for x in tempGroups if x.strip()]
                for group in tempAllGroups:
                    group = group.replace("www.facebook.com", "m.facebook.com")
                    self.groups.append(group)
                frame.setText(f'{frame.text()}\n {len(self.groups)} groups loaded')
                
                frame.setStyleSheet("color: green;")
            except Exception as e:
                frame.setText(f'error: {e}')
                frame.setStyleSheet("color: red;")


    def clearImagesVideos(self, frame):
        self.images.clear()
        frame.setText("All images have been cleared")
        frame.setStyleSheet("color: green;")
    
    def ClearGroups(self, frame):
        self.groups.clear()
        frame.setText("All groups have been cleared. Add another '.txt' file containing group links.")
        frame.setStyleSheet("color: green;")

    def getJoinedGroups(self, frame, keyword, maxGrp):
            frame.setText(f"Collectting some groups for the keyword {keyword}")
            frame.setStyleSheet("color: green;")
            self.driver.get(f'https://m.facebook.com/search/groups/?q={keyword}')
            time.sleep(5)
            if True:
                i = 1
                getGroups = True
                repeat = 1
                while getGroups:
                    try:
                        if (len(self.groups)>= maxGrp):
                            getGroups = False
                        path = f"/html[1]/body[1]/div[1]/div[1]/div[4]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[{i}]"
                        grpLink = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, path)))
                        grpLink.location_once_scrolled_into_view
                        grpLink.click()

                        try:
                            postStart = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(
                                (By.XPATH, '//div[starts-with(text(),"Write something")]')))
                        except Exception:
                            try:
                                postStart = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(
                                    (By.XPATH, '//div[starts-with(text(),"Create a public")]')))
                            except Exception:
                                try:
                                    postStart = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(
                                    (By.XPATH, '//div[starts-with(text(),"What\'s on your mind")]')))
                                except Exception:
                                    try:
                                        postStart = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(
                                        (By.XPATH, "//textarea[@id='uniqid_1']")))
                                    except Exception:
                                        try:
                                            postStart = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(
                                            (By.TAG_NAME, 'textarea')))
                                        except Exception as e:
                                            pass
                        if str(type(postStart)) == "<class 'selenium.webdriver.remote.webelement.WebElement'>":
                            self.groups.append(self.driver.current_url)
                        else:
                            print("You dont have permission to post to this group, so ignoring this group...")
                        self.driver.back()
                        
                        i = i+1
                        repeat = repeat * 0
                        frame.setText(f"Ok We have collected {len(self.groups)} groups so far")
                        frame.setStyleSheet("color: green;")
                        time.sleep(3)
                    except Exception as e:
                        repeat = repeat +1
                        if (repeat > 10):
                            getGroups = False
                        i = i+1
                        print("There was a issue processing this group, so ignoring... You can check logs.txt for details")
                        f = open("logs.txt", "a", encoding="utf-8")
                        f.write(
                        f'\n\n\n A group was ignored because of  \n {e}')
                        f.close()




class FacebookGroupPosterGUI(FaceBookGroupPoster):
    def __init__(self):
        self.main_win = QMainWindow()
        self.ui = Ui_Form()
        self.ui.setupUi(self.main_win)
        super().__init__()
        self.ui.statusText.setText("In a moment, The Chrome browser will open. Once opened login to your fb account.")
        self.ui.statusText.setStyleSheet("color: green;")
        self.ui.clearGrpsBtn.clicked.connect(lambda: self.ClearGroups(self.ui.statusText))
        self.ui.clearImages.clicked.connect(lambda:self.clearImagesVideos(self.ui.statusText))
        self.ui.addImageBtn.clicked.connect(lambda:self.getImages(self.ui.statusText))
        self.ui.addGrpBtn.clicked.connect(lambda:self.addGroups(self.ui.statusText))
        global msgG, frame, intervalG, keywordG, maxGrps, postToGroups
        msgG = self.ui.postText
        frame = self.ui.statusText
        intervalG =  self.ui.timer
        keywordG = self.ui.keyword
        maxGrps = self.ui.maxGrpToFetch
        self.ui.start.clicked.connect(self.startPosting)
        self.ui.exitBtn.clicked.connect(self.close)
        autoStart = threading.Thread(target=self.startFaceBookGroupPoster, args=(self.ui.statusText,"1"))
        autoStart.run()

    def startPosting(self):
        postToGroups = threading.Thread(target=self.postGroups)
        if postToGroups.is_alive():
            postToGroups.join()
            postToGroups.start()
        else:
            postToGroups.start()



    def show(self):
        self.main_win.show()

    def close(self):
        self.main_win.close()
        self.terminate()
        

