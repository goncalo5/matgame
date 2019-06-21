import random
import math

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy import properties as kp
from kivy.animation import Animation


LEVELS = {
    "exponent": 2,
    "options": [
        "naturals",
        "integers",
        "rationals",
        "reals",
        "complexs"
    ],
    "min_xp_unblock": {
        "negatives": 50,
        "fraction": 250,
        "irrational": 1250,
        "imaginary": 6250
    }
}
# MENU_MATTERS = {
#     "add_naturals_menu": "Naturals",
#     "add_integers_menu": "Integers (naturals + negatives)"
# }
MENU_MATTERS = {
    "add_naturals": "Naturals",
    "add_integers": "Integers (naturals + negatives)"
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
    current_matter_name = kp.StringProperty("add_naturals")
    current_matter_level = kp.NumericProperty(1)
    current_matter_xp = kp.NumericProperty(1)
    current_xp_to_add_label = kp.StringProperty("")

    # addition
    # Naturals
    add_naturals_level = kp.NumericProperty(1)
    add_naturals_counter = kp.NumericProperty(1)
    add_naturals_xp = kp.NumericProperty(0)
    # Întegers
    add_integers_level = kp.NumericProperty(1)
    add_integers_counter = kp.NumericProperty(1)
    add_integers_xp = kp.NumericProperty(0)

    def build(self):
        self.game = Game()
        return self.game
    
    def change_current_matter(self, new_matter):
        print("change_current_matter", new_matter)
        self.current_matter_name = new_matter
        self.update_currents()
        print("current", self.current_matter_level, self.current_matter_xp)

    def update_currents(self):
        if self.current_matter_name == "add_naturals":
            self.current_matter_level = self.add_naturals_level
            self.current_matter_xp = self.add_naturals_xp
        elif self.current_matter_name == "add_integers":
            self.current_matter_level = self.add_integers_level
            self.current_matter_xp = self.add_integers_xp

    def new_problem(self):
        print("new_problem")
        self.update_currents()

        if not self.can_next:
            return
        print("self.current_matter_name", self.current_matter_name)
        self.can_next = False
        self.can_check_option = True
        self.current_xp_to_add_label = ""
        _max = self.add_naturals_level**LEVELS.get("exponent", 2)
        if self.current_matter_name == "add_naturals":
            _min = 0
        if self.current_matter_name == "add_integers":
            _min = -self.add_naturals_level**LEVELS.get("exponent", 2)
        value1 = random.randint(_min, _max)
        value2 = random.randint(_min, _max)

        self.problem_label = str("{} + {}".format(value1, value2))
        self.correct_option = self.calc_result(value1, value2)

        self.update_options()
    
    def calc_result(self, value1, value2):
        return value1 + value2

    def update_options(self):
        res = {self.correct_option}
        _max = self.add_naturals_level**LEVELS.get("exponent", 2)
        if self.current_matter_name == "add_naturals":
            _min = 0
        if self.current_matter_name == "add_integers":
            _min = -self.add_naturals_level**LEVELS.get("exponent", 2)
        while len(res) < 3:
            value1 = random.randint(_min, _max)
            value2 = random.randint(_min, _max)
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
                self.msg_color = [0, 1, 0, 1]
                sign = "+"

                if self.current_matter_name == "add_naturals":
                    self.add_naturals_counter += 1
                    self.add_naturals_counter = max(self.add_naturals_counter, 1)
                    to_add = self.add_naturals_counter
                elif self.current_matter_name == "add_integers":
                    self.add_integers_counter += 1
                    self.add_integers_counter = max(self.add_integers_counter, 1)
                    to_add = self.add_integers_counter
            else:
                button.background_color = (1, 0, 0, 1)
                self.msg_color = [1, 0, 0, 1]
                sign = ""

                if self.current_matter_name == "add_naturals":
                    self.add_naturals_counter -= 1
                    self.add_naturals_counter = max(self.add_naturals_counter, 1)
                    to_add = -self.add_naturals_counter
                elif self.current_matter_name == "add_integers":
                    self.add_integers_counter -= 1
                    self.add_integers_counter = max(self.add_integers_counter, 1)
                    to_add = -self.add_integers_counter

            if self.current_matter_name == "add_naturals":
                self.add_naturals_xp += to_add

                Animation(current_matter_xp=self.add_naturals_xp, duration=0.5).start(self)
                self.current_xp_to_add_label = "{} {}".format(sign, to_add)
            elif self.current_matter_name == "add_integers":
                new_xp = self.add_integers_xp + to_add
                Animation(add_integers_xp=new_xp, duration=0.5).start(self)
                self.current_xp_to_add_label = "{} {}".format(sign, to_add)

            self.can_check_option = False
            self.can_next = True
    
    def on_add_naturals_xp(self, *args):
        self.add_naturals_xp = max(self.add_naturals_xp, 0)
        self.add_naturals_level = int((0.1 * self.add_naturals_xp)**0.5 + 1)
    
    def on_add_integers_xp(self, *args):
        self.add_integers_xp = max(self.add_integers_xp, 0)
        self.add_integers_level = int((0.1 * self.add_integers_xp)**0.5 + 1)


if __name__ == "__main__":
    MatGameApp().run()
