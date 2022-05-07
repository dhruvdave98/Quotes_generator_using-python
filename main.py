# -----------------------------------------------------------
# Demonstrates the application, which let the user sign-up and login into the app
# and enter how the user feel, according to that it will generate a quote from the file.
# This app has used python kivy library
#
# email dhruvdave61@gmail.com
# ----------------------------------------------------------

import glob
import json
import random
from pathlib import Path

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from datetime import datetime
from hoverable import HoverBehavior
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior

# it loads the design.kv, which contains the frontend(design) of the application
Builder.load_file('design.kv')


# by default the log in screen shows up, when the application loads
class LoginScreen(Screen):
    # sign-up button, which navigates to sign-up screen
    def sign_up(self):
        self.manager.current = "sign_up_screen"

    # login button, which checks the credentials entered by the user
    def login(self, uname, pword):
        with open("users.json") as file:
            users = json.load(file)
        if uname in users and users[uname]['password'] == pword:
            self.manager.current = "login_screen_success"
        else:
            self.ids.login_wrong.text = "Wrong username or password !"


# ScreenManager is used to navigate through multiple screens
class RootWidget(ScreenManager):
    pass


# sign-up screen asks the user to enter username and password in it and
# store it with date time in the users.json file
class SignUpScreen(Screen):
    def add_user(self, uname, pword):
        with open("users.json") as file:
            users = json.load(file)

        users[uname] = {'username': uname, 'password': pword,
                        'created': datetime.now().strftime("%Y-%m-%d %H-%M-%S")}

        with open("users.json", "w") as file:
            json.dump(users, file)
        self.manager.current = "sign_up_screen_success"


# sign-up screen success redirects the user to login screen
class SignUpScreenSuccess(Screen):
    def back_to_login(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"


# login screen success navigates users to the quote section where
# user can write their feeling and get the quote according to that
class LoginScreenSuccess(Screen):
    # log out button used to log out the user and navigate to the login screen
    def log_out(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"

    # get quote is used to get the quote according to the feelings entered by the user
    def get_quote(self, feel):
        feel = feel.lower()
        available_feelings = glob.glob("quotes/*txt")

        available_feelings = [Path(filename).stem for filename in available_feelings]

        if feel in available_feelings:
            with open(f"quotes/{feel}.txt", encoding="utf8") as file:
                quotes = file.readlines()
            self.ids.quote.text = random.choice(quotes)
        else:
            self.ids.quote.text = "Try another feeling"


# Logout is the ImageButton used log out the user
class ImageButton(ButtonBehavior, HoverBehavior, Image):
    pass


# builds the app
class MainApp(App):
    def build(self):
        return RootWidget()


if __name__ == "__main__":
    MainApp().run()
