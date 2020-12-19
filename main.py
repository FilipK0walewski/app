# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
# from kivy.core.audio import SoundLoader
# from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.core.window import Window
# from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.clock import Clock
# from kivy.properties import ObjectProperty, NumericProperty
# from kivy.graphics import *
import csv, os, random


class MenelApp(App):

    layout = None
    down_layout = None
    up_layout = None
    buttons = []
    btn1 = None
    btn2 = None
    btn3 = None
    btn4 = None
    btn5 = None
    label = None
    yellow = [255 / 255.0, 173 / 255.0, 1 / 255.0, 1.0]
    blue = [0, 0, 1, 1]
    green = [126 / 255.0, 200 / 255.0, 80 / 255.0, 1]
    red = [1, 0, 0, 1]
    questions = []
    question = None
    correct = None
    time = True

    def start_game(self):
        self.menu_animation_0()
        self.read_file('questions.csv')
        self.create_buttons()
        Clock.schedule_interval(self.timer_countdown, 1)

    def timer_countdown(self, dt):
        if self.root.ids.q.texture_size[0] > self.root.size[0]:
            self.add_line()

        if self.down_layout.opacity == 1 and self.time is True:
            temp = self.root.ids.timer.text
            temp = int(temp)
            temp -= 1
            self.root.ids.timer.text = str(temp)
            if temp == 0:
                self.game_over_0()
                self.correct = False

    def add_line(self):

        temp_bool = False
        i = 0
        temp = ''
        for sign in self.root.ids.q.text:
            if sign == ' ' and temp_bool is False:
                temp += '\n'
                temp_bool = True
            else:
                temp += sign
            i += 1

        self.root.ids.q.text = temp

    def menu_animation_0(self):
        anim = Animation(opacity=0, duration=1)
        anim.bind(on_complete=self.menu_animation_1)
        anim.start(self.root.ids.start_button)
        anim.start(self.root.ids.quit_button)

    def menu_animation_1(self, *args):
        anim = Animation(opacity=0, duration=1)
        anim.bind(on_complete=self.get_question)
        anim.start(self.root.ids.q)

    def create_buttons(self):

        self.down_layout = GridLayout(cols=2, pos=(0, Window.height / 5), size_hint=(1, .3), padding=[10, 10, 10, 10], spacing=[10, 10], opacity=0)

        self.btn1 = Button(text="A: ", on_release=self.answer_pressed)
        self.btn2 = Button(text="B: ", on_release=self.answer_pressed)
        self.btn3 = Button(text="C: ", on_release=self.answer_pressed)
        self.btn4 = Button(text="D: ", on_release=self.answer_pressed)
        self.buttons.append(self.btn1)
        self.buttons.append(self.btn2)
        self.buttons.append(self.btn3)
        self.buttons.append(self.btn4)

        for button in self.buttons:
            button.background_down = ''
            button.background_normal = ''
            button.background_color = self.blue
            button.font_name = 'Aleo-Regular.otf'
            button.background_disabled_normal = ''

        self.btn5 = Button(text="confirm", on_release=self.check_answer, background_color=[0, 0, 1, 1],
                           size_hint=(0.5, None), pos_hint={'x': 0.25, 'y': 0.02}, font_name='Aleo-Regular.otf',
                           disabled=True, opacity=0)

        self.down_layout.add_widget(self.btn1)
        self.down_layout.add_widget(self.btn2)
        self.down_layout.add_widget(self.btn3)
        self.down_layout.add_widget(self.btn4)

        self.up_layout = FloatLayout()
        self.up_layout.add_widget(self.btn5)

        self.root.add_widget(self.up_layout)
        self.root.add_widget(self.down_layout)

    def get_question(self, *args):
        self.reset_buttons()
        self.question = random.choice(self.questions)
        temp = [2, 3, 4, 5]
        i = 0
        for button in self.buttons:
            button.disabled = False
            i = random.choice(temp)
            temp.remove(i)
            button.text += self.question[i]

        self.root.ids.q.text = self.question[0]
        self.root.ids.timer.text = '30'
        self.animate_the_label()
        # self.animate_grid()
        # self.root.ids.q.text = self.question[0]

    def answer_pressed(self, instance):
        anim0 = Animation(background_color=self.blue, duration=0.5)
        for button in self.buttons:
            anim0.start(button)

        anim = Animation(opacity=1, duration=0.5)
        anim.start(self.btn5)
        self.btn5.disabled = False

        anim = Animation(background_color=self.yellow, duration=0.5)
        anim.start(instance)

    def check_answer(self, instance):
        self.time = False
        for button in self.buttons:
            button.disabled = True
            if button.background_color == self.yellow:
                answer = button.text[3:]
                if self.question[1] == answer:
                    self.questions.remove(self.question)
                    self.correct = True
                    self.animate_the_button(button)
                else:
                    self.correct = False
                    self.animate_the_button(button)

    def game_over_0(self, *args):
        anim = Animation(opacity=0, duration=2)
        if self.correct is True:
            anim.bind(on_complete=self.get_question)
        else:
            anim.bind(on_complete=self.game_over_1)

        anim.start(self.down_layout)
        anim.start(self.root.ids.q)
        anim.start(self.root.ids.timer)
        anim.start(self.btn5)

    def game_over_1(self, *args):
        self.buttons.clear()
        self.root.remove_widget(self.down_layout)
        self.root.remove_widget(self.up_layout)
        self.root.ids.q.text = "Pierdolnikerzy"
        self.root.ids.q.timer = "30"
        self.root.ids.start_button.disabled = False
        self.root.ids.quit_button.disabled = False
        anim = Animation(opacity=1, duration=2)
        anim.start(self.root.ids.q)
        anim.start(self.root.ids.start_button)
        anim.start(self.root.ids.quit_button)

    def reset_buttons(self):
        self.btn5.disabled = True
        for button in self.buttons:
            temp = button.text[0:3]
            button.text = temp
            button.background_color = self.blue

    def read_file(self, filename):
        with open(os.path.join(filename), encoding='utf8') as data:
            data = csv.reader(data, delimiter=',')
            for row in data:
                self.questions.append(list(row))

    def animate_the_button(self, button):
        if self.correct is True:
            color = self.green
        else:
            color = self.red

        anim = Animation(background_color=color, duration=0.1)
        for i in range(3):
            anim += Animation(background_color=self.blue, duration=0.5)
            anim += Animation(background_color=color, duration=0.5)

        anim.bind(on_complete=self.game_over_0)
        anim.start(button)

    def animate_the_label(self):
        anim = Animation(opacity=1, duration=2)
        anim.bind(on_complete=self.animate_grid)
        anim.start(self.root.ids.q)
        anim.start(self.root.ids.timer)

    def animate_grid(self, *args):
        anim = Animation(opacity=1, duration=2)
        # anim.bind(on_complete=self.animate_grid_cd)
        anim.start(self.down_layout)
        self.time = True


MenelApp().run()
