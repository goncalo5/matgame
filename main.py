import random

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy import properties as kp


levels = {
    1: [0, 1, 2],
    2: [0, 1, 2, 3, 4, 5]
}



class Menu(Screen):
    pass


class AddMenu(Screen):
    pass


class Game(ScreenManager):
    pass


class MatGameApp(App):
    # screen_manager = kp.ObjectProperty(None)
    player_level = kp.NumericProperty(1)
    add_level = kp.NumericProperty(0)
    problem_label = kp.StringProperty("")

    def build(self):
        self.game = Game()
        return self.game
    
    def new_problem_label(self):
        possibles = levels[self.player_level]
        value1 = random.choice(possibles)
        value2 = random.choice(possibles)

        self.problem_label = str("{} + {}".format(value1, value2))


if __name__ == "__main__":
    MatGameApp().run()
