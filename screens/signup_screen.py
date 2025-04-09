from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivymd.uix.dialog import MDDialog
from kivymd.app import MDApp

class SignUpScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def create_account(self):
        fullname = self.ids.signup_fullname.text
        uname = self.ids.signup_username.text
        pword = self.ids.signup_password.text
        confirm = self.ids.signup_confirm.text

        db = MDApp.get_running_app().db

        if not fullname or not uname or not pword or not confirm:
            MDApp.get_running_app().show_alert("Oops...", "All fields are required.")
        elif pword != confirm:
            MDApp.get_running_app().show_alert("Oops...", "Passwords do not match.")
        elif db.user_exists(uname):
            MDApp.get_running_app().show_alert("Oops...", "Username already exists.")
        else:
            db.create_user(fullname, uname, pword)
            MDApp.get_running_app().show_alert("Oops...", "Account created successfully.")
            self.manager.current = "login_screen"
