from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivy.core.window import Window

from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton

from database import DatabaseManager
from screens.login_screen import LoginScreen
from screens.signup_screen import SignUpScreen
from screens.welcome_screen import WelcomeScreen
from screens.home_screen import HomeScreen

class BurgerApp(MDApp):
    def build(self):
        # Start the app maximized instead of full screen
        Window.maximize()
        
        # Initialize database and theme
        self.db = DatabaseManager()
        self.theme_cls.primary_palette = "Red"

        # Load KV layout
        Builder.load_file("kv/burger.kv")

        # Setup screen manager
        sm = ScreenManager(transition=FadeTransition(duration=0.5))
        sm.add_widget(WelcomeScreen(name="welcome_screen"))
        sm.add_widget(LoginScreen(name="login_screen"))
        sm.add_widget(SignUpScreen(name="signup_screen"))
        sm.add_widget(HomeScreen(name="home_screen"))

        return sm

    def get_started(self):
        self.root.current = "login_screen"

    def go_to_signup(self):
        self.root.transition.direction = "left"
        self.root.current = "signup_screen"

    def go_back(self):
        self.root.transition.direction = "right"
        self.root.current = "login_screen"

    def show_alert(self, title, text):
        dialog = MDDialog(
                title=title,
                text=text,
                buttons=[MDFlatButton(text="Close", on_release=lambda x: dialog.dismiss())]
            )
        
        dialog.open()

if __name__ == '__main__':
    BurgerApp().run()
