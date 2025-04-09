from kivy.uix.screenmanager import Screen

class HomeScreen(Screen):
    current_user_full_name = ""  # Add this attribute to store the full name

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_enter(self):
        # This will ensure the welcome message and full name are updated when entering the screen
        welcome_label = self.ids.welcome_label
        welcome_label.text = f"Welcome, {self.current_user_full_name}!"

