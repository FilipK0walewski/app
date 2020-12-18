# -*- coding: utf-8 -*-
import codecs
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.core.audio import SoundLoader
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.properties import ObjectProperty, NumericProperty
from kivy.graphics import *
import csv, os, random


class Answers(GridLayout):

    def do_action(self):
        self.label_wid.text = 'After'


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
    yellow = [255 / 255.0, 255 / 255.0, 69 / 255.0, 1.0]
    blue = [0, 0, 1, 1]
    green = [1, 100 / 255.0, 0, 0]
    red = [1, 0, 0, 1]
    questions = []
    question = None

    def start_game(self):
        self.read_file('questions.csv')
        self.create_buttons()
        self.random_question()
        # self.temp()

    def create_buttons(self):

        self.down_layout = GridLayout(cols=2, pos=(0, Window.height / 5), size_hint=(1, .3))

        self.label = Label(text=self.questions[0][0], font_size='20sp', pos=(200, 500))

        self.btn1 = Button(text="A: ", on_release=self.answer_pressed, background_color=[0, 0, 1, 1], font_name='Aleo-Regular.otf')
        self.btn2 = Button(text="B: ", on_release=self.answer_pressed, background_color=[0, 0, 1, 1], font_name='Aleo-Regular.otf')
        self.btn3 = Button(text="C: ", on_release=self.answer_pressed, background_color=[0, 0, 1, 1], font_name='Aleo-Regular.otf')
        self.btn4 = Button(text="D: ", on_release=self.answer_pressed, background_color=[0, 0, 1, 1], font_name='Aleo-Regular.otf')
        self.btn5 = Button(text="confirm", on_release=self.check_answer, background_color=[0, 0, 1, 1],
                           size_hint=(0.5, None), pos_hint={'x': 0.25, 'y': 0}, font_name='Aleo-Regular.otf')

        self.buttons.append(self.btn1)
        self.buttons.append(self.btn2)
        self.buttons.append(self.btn3)
        self.buttons.append(self.btn4)
        # self.buttons.append(self.btn5)

        self.down_layout.add_widget(self.btn1)
        self.down_layout.add_widget(self.btn2)
        self.down_layout.add_widget(self.btn3)
        self.down_layout.add_widget(self.btn4)
        # self.down_layout.add_widget(self.btn5)

        self.up_layout = FloatLayout()
        self.up_layout.add_widget(self.btn5)
        # self.up_layout.add_widget(self.label)

        self.root.add_widget(self.up_layout)
        self.root.add_widget(self.down_layout)

    def random_question(self):
        self.question = random.choice(self.questions)

        self.root.ids.q.text = self.question[0]

        i = -1
        for button in self.buttons:
            button.text += self.question[i]
            i -= 1

    def answer_pressed(self, instance):
        for button in self.buttons:
            button.background_color = self.blue

        instance.background_color = self.yellow

    def check_answer(self, instance):
        for button in self.buttons:
            if button.background_color == self.yellow:
                answer = button.text[3:]
                if self.question[1] == answer:
                    button.background_color = [1, 1, 1, 1]
                    button.background_color = self.green
                    sound = SoundLoader.load('cudownie.wav')
                    if sound:
                        sound.play()
                    self.reset_buttons()
                    self.random_question()
                else:
                    button.background_color = self.red
                    sound = SoundLoader.load('slaby.wav')
                    if sound:
                        sound.play()

    def reset_buttons(self):
        for button in self.buttons:
            temp = button.text[0:3]
            button.text = temp

    def read_file(self, filename):
        with open(os.path.join(filename), encoding='utf8') as data:
            data = csv.reader(data, delimiter=',')
            for row in data:
                self.questions.append(list(row))


MenelApp().run()
