# ---------- INSTALLATION INSTRUCTIONS ----------
# To run this application, you need to install the required libraries.
# Use the following commands to install them:

# Install Kivy
# pip install kivy

# Install KivyMD
# pip install kivymd

# Install MySQL Connector for Python
# pip install mysql-connector-python

from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivymd.uix.dialog import MDDialog
from kivy.uix.image import Image
import mysql.connector

# ---------- DATABASE MANAGER ----------
class DatabaseManager:
    def __init__(self):
        self.config = {
            'user': 'root',           # Change to your MySQL user
            'password': '',           # Change to your MySQL password
            'host': 'localhost'
        }
        self.db_name = 'burger_app'
        self.table_name = 'users'
        self.init_database()

    def init_database(self):
        try:
            conn = mysql.connector.connect(**self.config)
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.db_name}")
            conn.database = self.db_name

            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {self.table_name} (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255),
                    username VARCHAR(255) UNIQUE,
                    password VARCHAR(255)
                )
            ''')
            conn.commit()
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")

    def validate_user(self, username, password):
        conn = mysql.connector.connect(database=self.db_name, **self.config)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {self.table_name} WHERE username=%s AND password=%s", (username, password))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result is not None

    def user_exists(self, username):
        conn = mysql.connector.connect(database=self.db_name, **self.config)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {self.table_name} WHERE username=%s", (username,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result is not None

    def create_user(self, name, username, password):
        conn = mysql.connector.connect(database=self.db_name, **self.config)
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO {self.table_name} (name, username, password) VALUES (%s, %s, %s)", (name, username, password))
        conn.commit()
        cursor.close()
        conn.close()

# ---------- KV STRING ----------
KV = '''
#:import FadeTransition kivy.uix.screenmanager.FadeTransition
#:import FloatLayout kivy.uix.floatlayout.FloatLayout

ScreenManager:
    transition: FadeTransition(duration=0.5)
    WelcomeScreen:
    LoginScreen:
    SignUpScreen:
    HomeScreen:

<WelcomeScreen>:
    name: "welcome_screen"
    FloatLayout:
        MDRaisedButton:
            text: "[b]Login[/b]"
            markup: True
            size_hint: 0.8, None
            height: "100dp"
            pos_hint: {"center_x": 0.5, "center_y": 0.16}
            on_release: app.get_started()
            md_bg_color: 0, 0, 0, 1
            text_color: 1, 1, 1, 1

        MDRaisedButton:
            text: "[b]Sign Up[/b]"
            markup: True
            size_hint: 0.8, None
            height: "100dp"
            pos_hint: {"center_x": 0.5, "center_y": 0.10}
            on_release: app.go_to_signup()
            md_bg_color: 1, 1, 1, 1
            text_color: 0, 0, 0, 1

<LoginScreen>:
    name: "login_screen"
    FloatLayout:
        MDBoxLayout:
            orientation: "vertical"
            padding: dp(20)
            spacing: dp(20)
            pos_hint: {"center_x": 0.5, "center_y": 0.65}

            
            MDCard:
                orientation: "vertical"
                padding: dp(20)
                spacing: dp(1)
                elevation: 10
                radius: [20]
                size_hint: None, None
                size: "350dp", "500dp"
                pos_hint: {"center_x": 0.5, "center_y": 0.5}  # <-- Centered here
                md_bg_color: 1, 1, 1, 0.8

                Image:
                    source: "logo2.jpeg"
                    size_hint_y: None
                    height: "120dp"

                MDLabel:
                    text: "Net's Burger Login"
                    halign: "center"
                    font_style: "H5"
                    color: 0.2, 0.2, 0.2, 1


                MDTextField:
                    id: login_username
                    hint_text: "Username"
                    mode: "rectangle"

                MDTextField:
                    id: login_password
                    hint_text: "Password"
                    password: True
                    mode: "rectangle"

                MDRaisedButton:
                    text: "[b]Login[/b]"
                    markup: True
                    size_hint: 0.6, None
                    height: "60dp"
                    pos_hint: {"center_x": 0.5}
                    on_release: root.validate_login()

                MDTextButton:
                    text: "Don't have an account? [color=0000FF]Sign up[/color]"
                    pos_hint: {"center_x": 0.5}
                    on_release: app.go_to_signup()
                    markup: True
                    text_color: 0, 0, 0, 1


<SignUpScreen>:
    name: "signup_screen"
    FloatLayout:
        MDBoxLayout:
            orientation: "vertical"
            padding: dp(20)
            spacing: dp(20)
            pos_hint: {"center_x": 0.5, "center_y": 0.60}

            MDCard:
                orientation: "vertical"
                padding: dp(20)
                spacing: dp(15)
                elevation: 10
                radius: [20]
                size_hint: None, None
                size: "350dp", "640dp"
                pos_hint: {"center_x": 0.5, "center_y": 0.5}  # <-- Centered here
                md_bg_color: 1, 1, 1, 0.8

                MDTextButton:
                    text: "[b]Back[/b]"
                    markup: True
                    size_hint: None, None
                    size: "100dp", "50dp"
                    pos_hint: {"top": 1, "right": 1}
                    on_release: app.go_back()
                    theme_text_color: "Custom"
                    text_color: 0.2, 0.2, 0.2, 1

                Image:
                    source: "logo2.jpeg"
                    size_hint_y: None
                    height: "120dp"

                MDLabel:
                    text: "Create Account"
                    halign: "center"
                    font_style: "H5"
                    color: 0.2, 0.2, 0.2, 1

                MDTextField:
                    id: signup_fullname
                    hint_text: "Full Name"
                    mode: "rectangle"

                MDTextField:
                    id: signup_username
                    hint_text: "New Username"
                    mode: "rectangle"

                MDTextField:
                    id: signup_password
                    hint_text: "Password"
                    password: True
                    mode: "rectangle"

                MDTextField:
                    id: signup_confirm
                    hint_text: "Confirm Password"
                    password: True
                    mode: "rectangle"

                MDRaisedButton:
                    text: "[b]Sign Up[/b]"
                    markup: True
                    size_hint: 0.6, None
                    height: "60dp"
                    pos_hint: {"center_x": 0.5}
                    on_release: root.create_account()


<HomeScreen>:
    name: "home_screen"
    MDBoxLayout:
        orientation: "vertical"
        padding: dp(40)
        spacing: dp(20)

        MDLabel:
            text: "Welcome to Net's Burger!"
            halign: "center"
            font_style: "H4"

        MDRaisedButton:
            text: "[b]Logout[/b]"
            markup: True
            size_hint: 0.6, None
            height: "60dp"
            pos_hint: {"center_x": 0.5}
            on_release: app.root.current = "login_screen"
'''

# ---------- SCREEN CLASSES ----------
class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        background = Image(source="logo3.jpeg", allow_stretch=True, keep_ratio=False)
        self.add_widget(background)

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        background = Image(source="logo1.jpeg", allow_stretch=True, keep_ratio=False)
        self.add_widget(background)

    def validate_login(self):
        uname = self.ids.login_username.text
        pword = self.ids.login_password.text
        db = MDApp.get_running_app().db
        if db.validate_user(uname, pword):
            self.manager.current = "home_screen"
        else:
            self.show_dialog("Login Failed", "Invalid credentials.")

    def show_dialog(self, title, text):
        dialog = MDDialog(title=title, text=text, size_hint=(0.8, None), height="200dp")
        dialog.open()

class SignUpScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        background = Image(source="logo1.jpeg", allow_stretch=True, keep_ratio=False)
        self.add_widget(background)

    def create_account(self):
        fullname = self.ids.signup_fullname.text
        uname = self.ids.signup_username.text
        pword = self.ids.signup_password.text
        confirm = self.ids.signup_confirm.text

        db = MDApp.get_running_app().db

        if not fullname or not uname or not pword or not confirm:
            self.show_dialog("Error", "All fields are required.")
        elif pword != confirm:
            self.show_dialog("Error", "Passwords do not match.")
        elif db.user_exists(uname):
            self.show_dialog("Error", "Username already exists.")
        else:
            db.create_user(fullname, uname, pword)
            self.show_dialog("Success", "Account created!")
            self.manager.current = "login_screen"

    def show_dialog(self, title, text):
        dialog = MDDialog(title=title, text=text, size_hint=(0.8, None), height="200dp")
        dialog.open()

class HomeScreen(Screen):
    pass

# ---------- MAIN APP ----------
class BurgerApp(MDApp):
    def build(self):
        self.db = DatabaseManager()
        return Builder.load_string(KV)

    def get_started(self):
        self.root.current = "login_screen"

    def go_to_signup(self):
        self.root.transition.direction = "left"
        self.root.current = "signup_screen"

    def go_back(self):
        self.root.transition.direction = "right"
        self.root.current = "login_screen"

if __name__ == '__main__':
    
    BurgerApp().run()