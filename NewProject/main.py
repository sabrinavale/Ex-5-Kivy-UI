import os
import kivy
import pygame
pygame.init()

#os.environ['DISPLAY'] = ":0.0"
#os.environ['KIVY_WINDOW'] = 'egl_rpi'

from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.animation import Animation
from kivy.uix.screenmanager import ScreenManager, Screen

from pidev.MixPanel import MixPanel
from pidev.kivy.PassCodeScreen import PassCodeScreen
from pidev.kivy.PauseScreen import PauseScreen
from kivy.clock import Clock
from pidev.kivy import DPEAButton
from pidev.kivy import ImageButton
from pidev.kivy.selfupdatinglabel import SelfUpdatingLabel

from pidev.Joystick import Joystick
joy = Joystick(0, True)
print(joy.get_axis('x'), joy.get_axis('y'))

from datetime import datetime

time = datetime

MIXPANEL_TOKEN = "x"
MIXPANEL = MixPanel("Project Name", MIXPANEL_TOKEN)

SCREEN_MANAGER = ScreenManager()
MAIN_SCREEN_NAME = 'main'
ADMIN_SCREEN_NAME = 'admin'


class ProjectNameGUI(App):
    """
    Class to handle running the GUI Application
    """

    def build(self):
        """
        Build the application
        :return: Kivy Screen Manager instance
        """
        return SCREEN_MANAGER


Window.clearcolor = (1, 1, 1, 1)  # White

class NewScreen(Screen):
    def image(self):
        SCREEN_MANAGER.current = 'main'

    def animation(self):
        #anim = Animation(x=50) + Animation(size=(80, 80), duration=2)
        anim = Animation(x=100, y=100) + Animation(duration=2)
        anim.start(self)


class MainScreen(Screen):
    """
    Class to handle the main screen and its associated touch events
    """
    def __init__(self, **kw):
        super().__init__(**kw)
        Clock.schedule_interval(self.joystick_update, 0.002)
    def joystick_update(self, dt):
        self.ids.axes.x = joy.get_axis('x') * self.width
        self.ids.axes.y = joy.get_axis('y') * self.height
        x = self.ids.axes.x
        y = self.ids.axes.y
        x = str(x)
        y = str(y)
        z = '(' + x + ', ' + y + ')'
        self.ids.axes.text = z


    def animation(self):
        #anim = Animation(x=50) + Animation(size=(80, 80), duration=2)
        anim = Animation(x=100, y=100) + Animation(duration=2)
        anim.start(self)


    def pressed(self):
        """
        Function called on button touch event for button with id: testButton
        :return: None
        """
        print("Callback from MainScreen.pressed()")

    def admin_action(self):
        """
        Hidden admin button touch event. Transitions to passCodeScreen.
        This method is called from pidev/kivy/PassCodeScreen.kv
        :return: None
        """
        SCREEN_MANAGER.current = 'passCode'

    def image(self):
        SCREEN_MANAGER.current = 'new'

    def text_change(self):
        if self.ids.test3.active:
            self.ids.test3.text = "Off"
            self.ids.test3.active = False
        else:
            self.ids.test3.text = "On"
            self.ids.test3.active = True

    def motor_change(self):
        if self.ids.motor_label.active:
            self.ids.motor_label.text = "motor off"
            self.ids.motor_label.active = False
        else:
            self.ids.motor_label.text = "motor on"
            self.ids.motor_label.active = True

    def increase(self):
        prior = self.ids.test4.text
        prior = int(prior)
        prior += 1
        self.ids.test4.text = str(prior)


class AdminScreen(Screen):
    """
    Class to handle the AdminScreen and its functionality
    """

    def __init__(self, **kwargs):
        """
        Load the AdminScreen.kv file. Set the necessary names of the screens for the PassCodeScreen to transition to.
        Lastly super Screen's __init__
        :param kwargs: Normal kivy.uix.screenmanager.Screen attributes
        """
        Builder.load_file('AdminScreen.kv')

        PassCodeScreen.set_admin_events_screen(ADMIN_SCREEN_NAME)  # Specify screen name to transition to after correct password
        PassCodeScreen.set_transition_back_screen(MAIN_SCREEN_NAME)  # set screen name to transition to if "Back to Game is pressed"

        super(AdminScreen, self).__init__(**kwargs)

    @staticmethod
    def transition_back():
        """
        Transition back to the main screen
        :return:
        """
        SCREEN_MANAGER.current = MAIN_SCREEN_NAME

    @staticmethod
    def shutdown():
        """
        Shutdown the system. This should free all steppers and do any cleanup necessary
        :return: None
        """
        os.system("sudo shutdown now")

    @staticmethod
    def exit_program():
        """
        Quit the program. This should free all steppers and do any cleanup necessary
        :return: None
        """
        quit()


"""
Widget additions
"""

Builder.load_file('main.kv')
SCREEN_MANAGER.add_widget(MainScreen(name=MAIN_SCREEN_NAME))
SCREEN_MANAGER.add_widget(PassCodeScreen(name='passCode'))
SCREEN_MANAGER.add_widget(PauseScreen(name='pauseScene'))
SCREEN_MANAGER.add_widget(AdminScreen(name=ADMIN_SCREEN_NAME))
SCREEN_MANAGER.add_widget(NewScreen(name='new'))

"""
MixPanel
"""


def send_event(event_name):
    """
    Send an event to MixPanel without properties
    :param event_name: Name of the event
    :return: None
    """
    global MIXPANEL

    MIXPANEL.set_event_name(event_name)
    MIXPANEL.send_event()


if __name__ == "__main__":
    # send_event("Project Initialized")
    # Window.fullscreen = 'auto'
    ProjectNameGUI().run()
