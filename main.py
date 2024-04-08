from pyngine import *
import pygame
import random
import math
import time

class Asteroid:
    MAXV = 200
    MAXR = 25
    COLOR = Color['gray']
    def __init__(self, controller, x=None, y=None, vx=None, vy=None, level=None):

        if x is None:
            self.x = random.randint(0, controller.screen_width)
            if random.randint(0, 1) == 0:
                self.x = 0
            else:
                self.x = controller.screen_width
        else:
            self.x = x

        if y is None:
            self.y = random.randint(0, controller.screen_height)
            if random.randint(0, 1) == 0:
                self.y = 0
            else:
                self.y = controller.screen_height
        else:
            self.y = y
        

        if vx is None:
            self.vx = random.randint(1, Asteroid.MAXV)
        else:
            self.vx = vx

        if vy is None:
            self.vy = random.randint(1, Asteroid.MAXV)
        else:
            self.vy = vy

        if level is None:
            self.level = random.randint(1, 2)
        else:
            self.level = level

        self.is_dead = self.level <= 0

    def take_damage(self, controller, asteroid_list):
        self.is_dead = True

        asteroid_list.append(Asteroid(controller, self.x, self.y, level=self.level-1))
        asteroid_list.append(Asteroid(controller, self.x, self.y, level=self.level-1))

    def collides(self, x, y, radius):
        min_distance = self.get_radius() + radius
        act_distance = math.sqrt((self.x - x)**2 + (self.y - y)**2)
        return act_distance <= min_distance

    def get_radius(self):
        return self.level * Asteroid.MAXR

    def update(self, controller):
        radius = self.get_radius()
        diameter = radius * 2

        self.x += self.vx * controller.delta_time
        if self.x < -diameter:
            self.x = controller.screen_width
        elif self.x > controller.screen_width + diameter:
            self.x = -diameter

        self.y += self.vy * controller.delta_time
        if self.y < -diameter:
            self.y = controller.screen_height + diameter
        elif self.y > controller.screen_height + diameter:
            self.y = -diameter

        radius = self.level * radius
        controller.painter.draw_circle(self.x, self.y, radius, Asteroid.COLOR)

class Ship:
    MAXV = 500
    MAXR = 25
    DELTAV = 30
    COLOR = Color['cadmiumorange']
    def __init__(self, controller, hp):
        self.x = random.randint(0, controller.screen_width)
        self.vx = 0
        self.y = random.randint(0, controller.screen_height)
        self.vy = 0

        self.hp = hp

        Event(controller, self.move_up, keys=(pygame.K_w))
        Event(controller, self.move_down, keys=(pygame.K_s))
        Event(controller, self.move_right, keys=(pygame.K_d))
        Event(controller, self.move_left, keys=(pygame.K_a))

    def take_damage(self):
        self.hp -= 10
    def get_radius(self):
        return Ship.MAXR
    def is_alive(self):
        return self.hp > 0

    def move_up(self):
        self.vy -= Ship.DELTAV
    def move_down(self):
        self.vy += Ship.DELTAV
    def move_right(self):
        self.vx += Ship.DELTAV
    def move_left(self):
        self.vx -= Ship.DELTAV

    def update(self, controller):
        radius = self.get_radius()
        diameter = radius * 2

        self.x += self.vx * controller.delta_time
        if self.x < -diameter:
            self.x = controller.screen_width
        elif self.x > controller.screen_width + diameter:
            self.x = -diameter

        self.y += self.vy * controller.delta_time
        if self.y < -diameter:
            self.y = controller.screen_height
        elif self.y > controller.screen_height + diameter:
            self.y = -diameter

        controller.painter.draw_circle(self.x, self.y, radius, Ship.COLOR)

class Bullet:
    MAXV = 300
    MAXR = 10
    COLOR = Color['red1']
    LIFESPAN = 3.0
    def __init__(self, x, y, tx, ty):
        self.x = x
        self.y = y

        self.angle = math.atan2(ty - y, tx - x)
        self.is_dead = False
        self.spawn_time = time.perf_counter()

    def is_alive(self):
        return not self.is_dead and (time.perf_counter() - self.spawn_time < Bullet.LIFESPAN)
    def get_radius(self):
        return Bullet.MAXR
    def take_damage(self):
        self.is_dead = True

    def update(self, controller):
        radius = self.get_radius()
        diameter = radius * 2

        self.x += math.cos(self.angle) * controller.delta_time * Bullet.MAXV
        if self.x < -diameter:
            self.x = controller.screen_width
        elif self.x > controller.screen_width + diameter:
            self.x = -diameter

        self.y += math.sin(self.angle) * controller.delta_time * Bullet.MAXV
        if self.y < -diameter:
            self.y = controller.screen_height
        elif self.y > controller.screen_height + diameter:
            self.y = -diameter

        controller.painter.draw_circle(self.x, self.y, radius, Bullet.COLOR)

class AsteroidsController(Controller):
    RELOAD_TIME = 0.2
    MAX_BULLETS = 5
    SCORE_BONUS = 100
    def __init__(self):
        Controller.__init__(self, tick_rate=1, debug=True, resolution=(900, 600))

        Drawer(self, refresh=self.draw)
        Event(self, action=self.force_damage, keys=(pygame.K_r))

        self.count = 5
        self.asteroids = [Asteroid(self) for _ in range(self.count)]

        self.ship = Ship(self, 30)

        self.health_label = Label(self, str(self.ship.hp))
        self.bullets = []
        self.last_shot = time.perf_counter()

        self.score = 0.0
        self.score_multiplier = 1.0
        self.score_label = Label(self, "_" * 20 + "Score: " + str(self.score))

    def draw(self):
        now = time.perf_counter()
        self.asteroids = list(filter(lambda asteroid: not asteroid.is_dead, self.asteroids))
        if not self.asteroids:
            self.count *= 2
            self.asteroids = [Asteroid(self) for _ in range(self.count)]
            self.ship.hp += 10
            self.score_multiplier *= 2.0

        for asteroid in self.asteroids:
            asteroid.update(self)
            if asteroid.collides(self.ship.x, self.ship.y, self.ship.get_radius()):
                asteroid.take_damage(self, self.asteroids)
                self.ship.take_damage()
                self.health_label.text = str(self.ship.hp)
                self.score_multiplier *= 0.8

            for bullet in self.bullets:
                if asteroid.collides(bullet.x, bullet.y, bullet.get_radius()):
                    asteroid.take_damage(self, self.asteroids)
                    bullet.take_damage()
                    self.score += AsteroidsController.SCORE_BONUS * self.score_multiplier

        self.bullets = list(filter(lambda bullet: bullet.is_alive(), self.bullets))
        for bullet in self.bullets:
            bullet.update(self)

        if self.ship.is_alive():
            self.ship.update(self)

            if self.mouse.presses[Mouse.l_click] and \
                    (now - self.last_shot > AsteroidsController.RELOAD_TIME) and \
                    len(self.bullets) < AsteroidsController.MAX_BULLETS:
                self.bullets.append(Bullet(self.ship.x, self.ship.y, self.mouse.x, self.mouse.y))
                self.last_shot = now
        else:
            self.health_label.text = "LOSER"

        self.score_label.text = "_" * 20 + "Score: " + str(self.score)

    def force_damage(self):
        babies = []
        for asteroid in self.asteroids:
            asteroid.take_damage(self, babies)
        self.asteroids.extend(babies)

if __name__ ==  '__main__':
    asteroids = AsteroidsController()
    asteroids.run()
