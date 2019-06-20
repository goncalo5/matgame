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
    option_1 = kp.NumericProperty(1)
    option_2 = kp.NumericProperty(1)
    option_3 = kp.NumericProperty(1)

    def build(self):
        self.game = Game()
        return self.game
    
    def new_problem(self):
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
            print("new", new, res)
        res = list(res)
        self.option_1 = res[0]
        self.option_2 = res[1]
        self.option_3 = res[2]
    
    def check_option(self, button):
        if int(button.text) == self.correct_option:
            button.background_color = (0, 1, 0, 1)
        else:
            button.background_color = (1, 0, 0, 1)




if __name__ == "__main__":
    MatGameApp().run()
