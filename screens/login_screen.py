from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def validate_login(self):
        uname = self.ids.login_username.text
        pword = self.ids.login_password.text
        
        db = MDApp.get_running_app().db

        if db.validate_user(uname, pword):
            # Fetch full name after successful login
            full_name = db.get_full_name(uname)  # Use a method to get the full name from the database
            self.manager.get_screen("home_screen").current_user_full_name = full_name  # Pass full name to HomeScreen
            self.manager.current = "home_screen"
        else:
            MDApp.get_running_app().show_alert("Login Failed", "Invalid credentials.")
