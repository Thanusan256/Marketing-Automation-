import threading
from time import sleep
from PyQt5.QtWidgets import QMainWindow
from instagram_private_api import Client as AppClient
import csv
from os import system, name
import sys
import os
from InstagramUI import Ui_Form



def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


targetUsername = None
email = None
password = None
followers = True
interval = None
status= None

def check_private_profile():
    return False

def getEmailFromFollowers(api, status):
    rank_token = AppClient.generate_uuid()
    username = targetUsername.text()
    global interval
    interval = int(interval.text())
    targetUser = api.username_info(username)
    filename = f'{username}_followers.csv'
    targetUserId = targetUser['user']['pk']
    data = api.user_followers(str(targetUserId), rank_token=rank_token)
    with open(filename, 'a', newline='') as csvfile:
        fieldnames = ['id', 'username', 'full_name', 'email']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'id': 'id',
                        'username': 'username',
                         'full_name': 'full_name',
                         'email': 'email'})
    for user in data.get('users', []):
        try:
            userEmailFinder = api.user_info(str(user['pk']))
            if 'public_email' in userEmailFinder['user'] and userEmailFinder['user']['public_email']:
                u = {
                    'id': user['pk'],
                    'username': user['username'],
                    'full_name': user['full_name'],
                    'email': userEmailFinder['user']['public_email']
                }
                with open(filename, 'a', newline='', encoding="utf-8") as csvfile:
                    fieldnames = ['id', 'username', 'full_name', 'email']
                    try:
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        writer.writerow(u)
                        status.setText(
                    '\x1b[6;30;42m' + f"Email of {user['username']} recorded" + '\x1b[0m')
                    except Exception:
                        status.setText("This user does not have a valid mail, trying another")
                
            else:
                status.setText(
                    f"{user['username']} did not contain any available email")
                
        except Exception as e:
            status.setText(f"AN ERROR OCCURED FOR {user['username']}: {e}")
    next_max_id = data.get('next_max_id')
    while next_max_id:
        if name == 'nt':
            _ = system('cls')
        # for mac and linux(here, os.name is 'posix')
        else:
            _ = system('clear')
        status.setText(f"Current users processed! Fetching new users after taking a break of {interval} seconds as you mentioned.")
        sleep(interval)
        try:
            data = api.user_followers(
                str(targetUserId), rank_token=rank_token, max_id=next_max_id)
            for user in data.get('users', []):
                userEmailFinder = api.user_info(str(user['pk']))
                if 'public_email' in userEmailFinder['user'] and userEmailFinder['user']['public_email']:
                    u = {
                        'id': user['pk'],
                        'username': user['username'],
                        'full_name': user['full_name'],
                        'email': userEmailFinder['user']['public_email']
                    }
                    with open(filename, 'a', newline='', encoding="utf-8") as csvfile:
                        fieldnames = ['id', 'username', 'full_name', 'email']
                        try:
                            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                            writer.writerow(u)
                            status.setText(
                         f"Email of {user['username']} recorded" )
                        except Exception:
                            status.setText("This user does not have a valid mail, trying another")
                    
                else:
                    status.setText(
                        f"{user['username']} did not contain any available email")

        except Exception as e:
            status.setText(f"AN ERROR OCCURED FOR {user['username']}: {e}")
        next_max_id = data.get('next_max_id')
    status.setText(
        f"Finished Processing, {filename} is saved in the current working directory")
    csvfile.close()


def getEmailFromFollowing(api, status):
    rank_token = AppClient.generate_uuid()
    username = targetUsername.text()
    global interval
    interval = int(interval.text())
    targetUser = api.username_info(username)
    filename = f'{username}_following.csv'
    targetUserId = targetUser['user']['pk']
    data = api.user_following(str(targetUserId), rank_token=rank_token)
    with open(filename, 'a', newline='') as csvfile:
        fieldnames = ['id', 'username', 'full_name', 'email']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'id': 'id',
                        'username': 'username',
                         'full_name': 'full_name',
                         'email': 'email'})
    
    for user in data.get('users', []):
            try:
                userEmailFinder = api.user_info(str(user['pk']))
                if 'public_email' in userEmailFinder['user'] and userEmailFinder['user']['public_email']:
                    u = {
                        'id': user['pk'],
                        'username': user['username'],
                        'full_name': user['full_name'],
                        'email': userEmailFinder['user']['public_email']
                    }
                    with open(filename, 'a', newline='', encoding="utf-8") as csvfile:
                            fieldnames = ['id', 'username', 'full_name', 'email']
                            try:
                                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                                writer.writerow(u)
                                status.setText(
                        f"Email of {user['username']} recorded")
                            except Exception:
                                status.setText("This user does not have a valid mail, trying another")
                    
                    
                else:
                    status.setText(
                        f"{user['username']} did not contain any available email")

            except Exception as e:
                status.setText(f"AN ERROR OCCURED FOR {user['username']}: {e}")
    next_max_id = data.get('next_max_id')
    while next_max_id:
        if name == 'nt':
            _ = system('cls')
        # for mac and linux(here, os.name is 'posix')
        else:
            _ = system('clear')
        print(f"Current users processed! Fetching new users after taking a break of {interval} seconds as you mentioned.")
        sleep(interval)
        try:
            data = api.user_following(
                str(targetUserId), rank_token=rank_token, max_id=next_max_id)
            for user in data.get('users', []):
                    userEmailFinder = api.user_info(str(user['pk']))
                    if 'public_email' in userEmailFinder['user'] and userEmailFinder['user']['public_email']:
                        u = {
                            'id': user['pk'],
                            'username': user['username'],
                            'full_name': user['full_name'],
                            'email': userEmailFinder['user']['public_email']
                        }
                        with open(filename, 'a', newline='', encoding="utf-8") as csvfile:
                            fieldnames = ['id', 'username', 'full_name', 'email']
                            try:
                                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                                writer.writerow(u)
                                status.setText(
                            f"Email of {user['username']} recorded")
                            except Exception:
                                status.setText("This user does not have a valid mail, trying another")
                        
                    else:
                        print(
                            f"{user['username']} did not contain any available email")

        except Exception as e:
            status.setText(f"AN ERROR OCCURRED FOR {user['username']}: {e}")
        next_max_id = data.get('next_max_id')
    status.setText(
        f"Finished Processing, {filename} is saved in the current working directory")
    csvfile.close()



class InstagramEmailScraperGUI:
    def __init__(self) -> None:
        self.main_win = QMainWindow()
        self.ui = Ui_Form()
        self.ui.setupUi(self.main_win)
        global targetUsername, email, password, interval, status
        status = self.ui.statusText
        targetUsername = self.ui.targetAudienceUserName
        email = self.ui.username
        password = self.ui.password
        interval = self.ui.timer
        self.ui.followersRadioBtn.clicked.connect(lambda: self.enableFollowers())
        self.ui.followingRadioBtn.clicked.connect(lambda: self.enableFollowing())
        self.ui.start.clicked.connect(self.extractEmails)
        self.ui.exitBtn.clicked.connect(self.close)

    def show(self):
        self.main_win.show()

    def close(self):
        self.main_win.close()

    def enableFollowers(self):
        global followers
        followers = False

    def enableFollowing(self):
        global followers
        followers = False

    def extractEmails(self):
        extractEmailProcess = threading.Thread(target=self.run)
        if extractEmailProcess.is_alive():
            extractEmailProcess.join()
            extractEmailProcess.start()
        else:
            extractEmailProcess.start()


    def run(self):     
        status.setText("Process Started")
        #validation for interval
        try:
            int(interval.text())
        except ValueError:
            status.setText("Please enter a number as value as timout")
            status.setStyleSheet("color: red;")
            return
        
        #validation for username & password
        if len(email.text()) <= 1:
                status.setText("Please enter a valid username")
                status.setStyleSheet("color: red;")
                return
        if len(password.text()) <= 1:
                status.setText("Please enter a valid password")
                status.setStyleSheet("color: red;")
                return
        if len(targetUsername.text()) <= 1:
                status.setText("Please enter a valid target username")
                status.setStyleSheet("color: red;")
                return
            

        
        self.ui.start.deleteLater()
        try:
            api = AppClient(auto_patch=True, authenticate=True,
                        username=email.text(), password=password.text())
            status.setText("Successfully Loginned to Instagram")
        except Exception as excp:
            status.setText(f"Cannot login to instagram, Ensure that your credential are correct \n {excp}")
            

        if check_private_profile():
            return print("This is a private profile. We are sorry")
        global followers
        if followers:
            self.ui.statusText.setText(f'Starting to extract followers of {self.ui.targetAudienceUserName.text()}')
            getEmailFromFollowers(api, status)
        else:
            self.ui.statusText.setText(f'Starting to extract following of {self.ui.targetAudienceUserName.text()}')
            getEmailFromFollowing(api, status)

        self.ui.statusText.setText("All done, Check current directory for OUTPUT")
        print("ALL DONE NOW YOU CAN OPEN THE CSV FILE IN CURRENT WORKING DIRECTORY")






