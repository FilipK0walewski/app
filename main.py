from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.uix.label import CoreLabel
from kivy.properties import ObjectProperty, NumericProperty
import random


class Background(Widget):
    star_texture = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # textures
        # self.star_texture = Image(source="assets/bomb_0.png").texture

    def scroll_textures(self, time_passed):
        print("scroll")


class Player(Image):
    move = False
    touch = None
    velocity = NumericProperty(0)

    def on_touch_down(self, touch):
        self.velocity = 200
        self.move = True
        self.touch = touch

    def on_touch_up(self, touch):
        self.move = False

"""
class Bomb(Widget):
    bomb_texture = ObjectProperty(None)
    velocity = NumericProperty(400)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bomb_texture = Image(source="assets/bomb_0.png").texture
        self.bomb_texture.wrap = 'repeat'
        self.bomb_texture.uvsize = (32, 32)

    def falling(self, dt):
        self.bomb_texture.uvpos = (self.bomb_texture.uvpos[0], self.bomb_texture.uvpos[1] + dt)
        print(self.bomb_texture.uvpos)
        texture = self.property('bomb_texture')
        texture.dispatch(self)
"""

"""
class GameWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.move = False
        self._touch = []
        self.bombs = []
        self.explosions = []
        self.temp_rect = None

        Window.clearcolor = (12/255.0, 22/255.0, 79/255.0, 1)

        with self.canvas:
            self.player = Rectangle(source="assets/player.png", pos=(0, 0), size=(32, 32))

        Clock.schedule_interval(self.move_step, 0)
        Clock.schedule_interval(self.drop_bomb, 2)
        Clock.schedule_interval(self.move_bomb, 0)
        Clock.schedule_interval(self.boom_animation, 0.1)

    def on_touch_down(self, touch):
        self.move = True
        self._touch.append(touch)

    def on_touch_up(self, touch):
        self.move = False
        self._touch.clear()

    def move_step(self, dt):
        current_x = self.player.pos[0]
        current_y = self.player.pos[1]

        step_size = 240 * dt
        if self.move is True:
            if self._touch[0].x < self.width / 3:
                current_x -= step_size
            if self._touch[0].x > 2 * self.width / 3:
                current_x += step_size

        if current_x < 0:
            current_x = 0
        if current_x + self.player.size[0] > self.width:
            current_x = self.width - self.player.size[0]
        self.player.pos = (current_x, current_y)

    def reset_canvas(self):
        self.canvas.clear()
        self.canvas.add(self.player)
        for bomb in self.bombs:
            self.canvas.add(bomb)

    def drop_bomb(self, dt):
        drop_x = random.randint(0, self.width - self.player.size[0])
        self.bombs.append(Rectangle(source="assets/bomb_0.png", pos=(drop_x, self.height + 32), size=(32, 32)))
        self.canvas.add(self.bombs[-1])

    def move_bomb(self, dt):
        drop_size = 240 * dt
        if len(self.bombs) != 0:
            for bomb in self.bombs:
                bomb_x = bomb.pos[0]
                bomb_y = bomb.pos[1] - drop_size
                temp_tuple = (bomb_x, bomb_y)
                bomb.pos = temp_tuple

                if bomb.pos[1] + bomb.size[1] < 0:
                    self.bombs.remove(bomb)

                if collides((self.player.pos, (self.player.size[0], self.player.size[1] - 16)),
                            (bomb.pos, bomb.size)) is True:
                    print("bum")
                    self.explosions.append([bomb.pos, bomb.size, 0])
                    self.bombs.remove(bomb)
                    self.canvas.remove(bomb)

    def boom_animation(self, dt):
        if len(self.explosions) != 0:
            for e in self.explosions:
                print(e)
                rect = Rectangle(source="assets/explosion/explosion_" + str(e[2]) + ".png", pos=(e[0]), size=e[1])
                self.canvas.add(rect)
                e[2] += 1
                if e[2] == 7:
                    self.explosions.remove(e)
                    self.reset_canvas()
    """


class MyApp(App):
    bombs = []
    gravity = 300
    frames = None
    player = None
    counter = 0

    def start_game(self):
        self.root.ids.start_button.disabled = True
        self.root.ids.quit_button.disabled = True
        self.root.ids.quit_button.opacity = 0
        self.root.ids.score.text = "0"
        self.counter = 0

        self.frames = Clock.schedule_interval(self.next_frame, 1/60.)

    def next_frame(self, dt):
        # Clock.schedule_interval(self.root.ids.background.scroll_textures, 1)
        self.move_player(dt)
        self.move_bombs(dt)
        if self.counter == 0:
            self.spawn_bomb()
        self.counter += 1
        if self.counter == 60:
            self.counter = 0

    def move_player(self, dt):
        self.player = self.root.ids.player
        if self.player.move is True:
            if self.player.touch.x < self.root.width / 3:
                self.player.x = self.player.x - self.player.velocity * dt
            if self.player.touch.x > 2 * self.root.width / 3:
                self.player.x = self.player.x + self.player.velocity * dt

            if self.player.x < 0:
                self.player.x = 0
            if self.player.x + self.player.size[0] > self.root.width:
                self.player.x = self.root.width - self.player.size[0]

    def move_bombs(self, dt):
        temp_y = None
        for bomb in self.bombs:
            temp_y = bomb.pos[1]
            bomb.pos = (bomb.pos[0], temp_y - dt * 120)

            if bomb.pos[1] + bomb.size[1] < 0:
                self.root.canvas.remove(bomb)
                self.bombs.remove(bomb)

            if self.check_collision((bomb.pos, bomb.size)) is True:
                self.root.canvas.remove(bomb)
                self.bombs.remove(bomb)
                self.game_over()

    def spawn_bomb(self):
        drop_x = random.randint(0, self.root.width - 32)
        bomb = Rectangle(source="assets/bomb_0.png", pos=(drop_x, self.root.height + 32), size=(32, 32))

        self.bombs.append(bomb)
        self.root.canvas.add(bomb)

    def game_over(self):
        self.root.ids.player.pos = (self.root.width / 2.0 - 16, 16)
        for bomb in self.bombs:
            self.root.canvas.remove(bomb)

        self.bombs.clear()
        self.frames.cancel()
        self.root.ids.start_button.disabled = False
        self.root.ids.start_button.opacity = 1

        self.root.ids.quit_button.disabled = False
        self.root.ids.quit_button.opacity = 1

    def check_collision(self, rect2):
        rect1 = ((self.player.pos[0], self.player.pos[1] - 16), self.player.size)
        r1x = rect1[0][0]
        r1y = rect1[0][1]
        r2x = rect2[0][0]
        r2y = rect2[0][1]
        r1w = rect1[1][0]
        r1h = rect1[1][1]
        r2w = rect2[1][0]
        r2h = rect2[1][1]

        if (r1x < r2x + r2w) and (r1x + r1w > r2x) and (r1y < r2y + r2h) and (r1y + r1h > r2y):
            return True
        else:
            return False


MyApp().run()
