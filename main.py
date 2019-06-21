import random
import math

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy import properties as kp
from kivy.animation import Animation


levels = {
    1: [0, 1, 2],
    2: [0, 1, 2, 3, 4, 5]
}

LEVELS = {
    "exponent": 2,
    "options": [
        "natural",
        "integer",
        "rational",
        "real",
        "complex"
    ],
    "min_xp_unblock": {
        "negatives": 50,
        "fraction": 250,
        "irrational": 1250,
        "imaginary": 6250
    }
}


class Menu(Screen):
    pass


class AddMenu(Screen):
    pass


class GameMenu(Screen):
    pass


class Game(ScreenManager):
    pass


class MatGameApp(App):
    player_level = kp.NumericProperty(1)
    player_xp = kp.NumericProperty(0)
    # 
    problem_label = kp.StringProperty("")
    option_1 = kp.NumericProperty(1)
    option_2 = kp.NumericProperty(1)
    option_3 = kp.NumericProperty(1)
    can_check_option = kp.BooleanProperty(True)
    can_next = kp.BooleanProperty(True)
    msg_color = kp.ListProperty([0,1,0,1])
    options = kp.ListProperty(LEVELS.get("options"))
    # add
    add_level = kp.NumericProperty(1)
    add_counter = kp.NumericProperty(1)
    add_xp = kp.NumericProperty(0)
    add_xp_to_add_label = kp.StringProperty("")

    def build(self):
        self.game = Game()
        return self.game
    
    def new_problem(self):
        if not self.can_next:
            return
        self.can_next = False
        self.can_check_option = True
        self.add_xp_to_add_label = ""
        possibles = levels[self.player_level]
        value1 = random.choice(possibles)
        value2 = random.choice(possibles)

        self.problem_label = str("{} + {}".format(value1, value2))
        self.correct_option = self.calc_result(value1, value2)

        self.update_options(possibles)
    
    def calc_result(self, value1, value2):
        return value1 + value2

    def update_options(self, possibles):
        res = {self.correct_option}
        while len(res) < 3:
            value1 = random.choice(possibles)
            value2 = random.choice(possibles)
            new = self.calc_result(value1, value2)
            res.add(new)
        res = list(res)
        self.option_1 = res[0]
        self.option_2 = res[1]
        self.option_3 = res[2]
    
    def check_option(self, button):
        if self.can_check_option:
            if int(button.text) == self.correct_option:
                button.background_color = (0, 1, 0, 1)
                self.add_counter += 1
                self.add_counter = max(self.add_counter, 1)
                to_add = self.add_counter
                self.msg_color = [0, 1, 0, 1]
                sign = "+"
            else:
                button.background_color = (1, 0, 0, 1)
                self.add_counter -= 1
                self.add_counter = max(self.add_counter, 1)
                to_add = -self.add_counter
                self.msg_color = [1, 0, 0, 1]
                sign = ""
            new_xp = self.add_xp + to_add

            Animation(add_xp=new_xp, duration=0.5).start(self)

            self.add_xp_to_add_label = "{} {}".format(sign, to_add)
            self.can_check_option = False
            self.can_next = True
    
    def on_add_xp(self, *args):
        self.add_xp = max(self.add_xp, 0)
        self.add_level = int((0.1 * self.add_xp)**0.5 + 1)


if __name__ == "__main__":
    MatGameApp().run()
