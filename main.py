import random
import math

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy import properties as kp
from kivy.animation import Animation
from kivy.event import EventDispatcher


LEVELS = {
    "exponent": 2,
    "addition": {
        "naturals": {
            "cost": 0
        },
        "integers": {
            "cost": 0
        }
    },
    "subtraction": {
        "naturals": {
            "cost": 10
        },
        "integers": {
            "cost": 50
        }
    },
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

MENU_MATTERS = {
    "add_naturals": "Naturals",
    "add_integers": "Integers (naturals + negatives)"
}

LIST_OF_SUBMATTER = ["naturals", "integers"]

class Menu(Screen):
    pass


class MatterMenu(Screen):
    pass


class GameMenu(Screen):
    pass


class Game(ScreenManager):
    pass


class Naturals(EventDispatcher):
    level = kp.NumericProperty(1)
    counter = kp.NumericProperty(1)
    xp = kp.NumericProperty(0)
    is_locked = kp.BooleanProperty(True)

    def __init__(self, cost, **kwargs):
        super().__init__(**kwargs)
        self.cost = cost


class Integers(EventDispatcher):
    level = kp.NumericProperty(1)
    counter = kp.NumericProperty(1)
    xp = kp.NumericProperty(0)
    is_locked = kp.BooleanProperty(True)

    def __init__(self, cost, **kwargs):
        super().__init__(**kwargs)
        self.cost = cost


class Addition(EventDispatcher):
    naturals = kp.ObjectProperty(Naturals(LEVELS["addition"]["naturals"]["cost"]))
    integers = kp.ObjectProperty(Integers(LEVELS["addition"]["integers"]["cost"]))


class Subtraction(EventDispatcher):
    naturals = kp.ObjectProperty(Naturals(LEVELS["subtraction"]["naturals"]["cost"]))
    integers = kp.ObjectProperty(Integers(LEVELS["subtraction"]["integers"]["cost"]))


class MatGameApp(App):
    player_level = kp.NumericProperty(1)
    player_xp = kp.NumericProperty(0)
    player_gold = kp.NumericProperty(0)
    # labels:
    labels_submatters_xp = kp.ListProperty([0, 0])
    labels_submatters_level = kp.ListProperty([0, 0])
    labels_submatters_cost = kp.ListProperty([0, 0])

    problem_label = kp.StringProperty("")
    list_options = kp.ListProperty([0, 0, 0])

    can_check_option = kp.BooleanProperty(True)
    can_next = kp.BooleanProperty(True)
    msg_color = kp.ListProperty([0,1,0,1])
    current_matter_name = kp.StringProperty("add_naturals")
    current_submatter_name = kp.StringProperty("naturals")
    current_matter_level = kp.NumericProperty(1)
    current_submatter_level = kp.NumericProperty(1)
    current_matter_xp = kp.NumericProperty(1)
    current_submatter_xp = kp.NumericProperty(1)
    current_xp_to_add_label = kp.StringProperty("")

    addition = kp.ObjectProperty(Addition())
    subtraction = kp.ObjectProperty(Subtraction())

    def build(self):
        self.game = Game()
        return self.game

    def clean_buttons(self, buttons):
        for button in buttons:
            button.background_color = 1,1,1,1
    
    def try_change_to_game_menu(self, submatter_name):
        print("try_change_to_game_menu", submatter_name)
        
        submatter = getattr(self.matter, submatter_name)

        print("cost", submatter.cost)
        if submatter.is_locked:

            if submatter.cost <= self.player_gold:

                self.player_gold -= submatter.cost
                submatter.is_locked = False
            else:
                print("you dont have enough gold, sorry")
                return

        self.game.transition.direction = 'left'
        self.game.current = "game_menu"
        self.current_submatter_name = submatter_name
        
        self.new_problem()
        self.update_labels()

    
    def update_labels(self):
        print("current_matter_name", self.current_matter_name)
        print("current_submatter_name", self.current_submatter_name)
        matter = getattr(self, self.current_matter_name)
        submatter = getattr(matter, self.current_submatter_name)
        self.matter = matter
        self.submatter = submatter
        for i, submatter_name in enumerate(LIST_OF_SUBMATTER):
            self.labels_submatters_xp[i] = getattr(matter, submatter_name).xp
            self.labels_submatters_level[i] = getattr(matter, submatter_name).level
            self.labels_submatters_cost[i] = getattr(matter, submatter_name).cost
        self.current_submatter_xp = submatter.xp
        self.current_submatter_level = submatter.level

    def on_current_matter_name(self, *args):
        print("list_options", dir(self))
        self.update_labels()

    def calc_min_and_max(self):
        _max = self.submatter.level**LEVELS.get("exponent", 2)
        if self.current_submatter_name == "naturals":
            _min = 0
        if self.current_submatter_name == "integers":
            _min = -_max
        return _min, _max

    def new_problem(self):
        print("new_problem")
        print("self.current_matter_name", self.current_matter_name)
        print("self.current_submatter_name", self.current_submatter_name)
        self.update_labels()

        if not self.can_next:
            return
        print("self.current_matter_name", self.current_matter_name)
        print("self.current_submatter_name", self.current_submatter_name)
        self.can_next = False
        self.can_check_option = True
        self.current_xp_to_add_label = ""
        n_of_values = 2
        _min, _max = self.calc_min_and_max()
        values = []
        for i in range(n_of_values):
            values.append(random.randint(_min, _max))

        map_matter2sign = {
            "addition": "+",
            "subtraction": "-",
            "multiplication": "x",
            "divison": "/",
        }
        sign = map_matter2sign.get(self.current_matter_name)
        values_to_show = []
        for i, value in enumerate(values):
            print("value", value)
            values_to_show.append("(%s)" % value if value < 0 else value)
        self.problem_label = str("{} {} {}".format(values_to_show[0], sign, values_to_show[1]))

        print("values", values)
        self.correct_option = self.calc_result(values[0], values[1])
        print("correct", self.correct_option)

        self.update_options()
    
    def calc_result(self, value1, value2):
        if self.current_matter_name == "addition":
            res = value1 + value2
        elif self.current_matter_name == "subtraction":
            res = value1 - value2
        print("res", res)
        return res

    def update_options(self):
        res = {self.correct_option}
        _min, _max = self.calc_min_and_max()
        while len(res) < 3:
            value1 = random.randint(_min, _max)
            value2 = random.randint(_min, _max)
            new = self.calc_result(value1, value2)
            res.add(new)
        self.list_options = list(res)
        print("res", res)
    
    def check_option(self, button):
        print()
        print()
        print()
        print("check_option")
        print(1)
        print("current_matter_name", self.current_matter_name)
        print("current_submatter_name", self.current_submatter_name)
        print("addition natural", self.addition.naturals.xp)
        print("addition integer", self.addition.integers.xp)
        print("subtraction natural", self.subtraction.naturals.xp)
        print("subtraction integer", self.subtraction.integers.xp)
        if not self.can_check_option:
            return

        if "add" in self.current_matter_name:
            print("addition")
            matter = self.addition
        elif "subtraction" in self.current_matter_name:
            print("subtraction")
            matter = self.subtraction

        if self.current_submatter_name == "naturals":
            print("naturals")
            submatter = matter.naturals
        elif self.current_submatter_name == "integers":
            print("integers")
            submatter = matter.integers

        print("matter", matter)
        print("submatter", submatter)

        if int(button.text) == self.correct_option:
            button.background_color = (0, 1, 0, 1)
            self.msg_color = [0, 1, 0, 1]
            sign = "+"

            submatter.counter += 1
            submatter.counter = max(submatter.counter, 1)
            to_add = submatter.counter

        else:
            button.background_color = (1, 0, 0, 1)
            self.msg_color = [1, 0, 0, 1]
            sign = ""

            submatter.counter -= 1
            submatter.counter = max(submatter.counter, 1)
            to_add = -submatter.counter


        print(2)
        print("addition natural", self.addition.naturals.xp)
        print("addition integer", self.addition.integers.xp)
        print("subtraction natural", self.subtraction.naturals.xp)
        print("subtraction integer", self.subtraction.integers.xp)
        print("matter", matter)
        print("submatter", submatter)

        submatter.xp += to_add
        Animation(current_submatter_xp=submatter.xp, duration=0.5).start(self)
        Animation(player_gold=self.player_gold + to_add, duration=0.5).start(self)
        self.current_xp_to_add_label = "{} {}".format(sign, to_add)

        self.can_check_option = False
        self.can_next = True
    

        print(3)
        print("addition natural", self.addition.naturals.xp)
        print("addition integer", self.addition.integers.xp)
        print("subtraction natural", self.subtraction.naturals.xp)
        print("subtraction integer", self.subtraction.integers.xp)
        submatter.xp = max(submatter.xp, 0)
        submatter.level = int((0.1 * submatter.xp)**0.5 + 1)

        self.update_labels()


if __name__ == "__main__":
    MatGameApp().run()
