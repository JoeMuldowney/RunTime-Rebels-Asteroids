from utils import get_random_position
from models import Spaceship, Asteroid

def restart_game(self, level):
    self.asteroids.clear()
    self.bullets.clear()
    self.upgrades.clear()
    self.active_upgrade = None
    self.upgrade_end_time = 0
    self.last_shot = 0
    self.message = ""

    for _ in range(level):
        while True:
            position = get_random_position(self.screen)
            if position.distance_to(self.spaceship.position) > self.MIN_ASTEROID_DISTANCE:
                break
        self.asteroids.append(Asteroid(position, self.asteroids.append))

def retry_game(self, level):
    self.asteroids.clear()
    self.bullets.clear()
    self.upgrades.clear()
    self.score = 0
    self.spaceship = Spaceship((400, 300), self.bullets.append)
    self.active_upgrade = None
    self.upgrade_end_time = 0
    self.last_shot = 0
    self.message = ""

    for _ in range(level):
        while True:
            position = get_random_position(self.screen)
            if position.distance_to(self.spaceship.position) > self.MIN_ASTEROID_DISTANCE:
                break
        self.asteroids.append(Asteroid(position, self.asteroids.append))