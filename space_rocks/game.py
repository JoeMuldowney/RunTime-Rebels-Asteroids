import pygame
import os
import sys
from utils import get_random_position, load_sprite, print_text
from models import Asteroid, Spaceship
from upgrade import Upgrade #new import
from menu import main_menu
from leader_board import save_score, get_player_name
# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

class SpaceRocks:
    MIN_ASTEROID_DISTANCE = 250
    UPGRADE_DESPAWN_TIME = 10000 #10 second despawn time
    
    def __init__(self):
        self._init_pygame()
        self.screen = pygame.display.set_mode((1550, 900))
        self.background = load_sprite("space", False)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 64)
        self.message = ""
        self.asteroids = []
        self.bullets = []
        self.upgrades = [] # New list for upgrades
        self.score = 0  # Initializing score
        self.spaceship = Spaceship((400, 300), self.bullets.append)
        self.active_upgrade = None #tracker
        self.upgrade_end_time = 0 #expiration time
        self.last_shot = 0
        self.running = True
        
        for _ in range(6):
            while True:
                position = get_random_position(self.screen)
                if position.distance_to(self.spaceship.position) > self.MIN_ASTEROID_DISTANCE:
                    break
            self.asteroids.append(Asteroid(position, self.asteroids.append))

    def main_loop(self):
        main_menu(self.screen, self.font)  # Call the menu function
        while self.running:
            self._handle_input()
            self._process_game_logic()
            self._draw()
    
    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Space Rocks")
    
    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.running = False
                pygame.quit()
            #elif self.spaceship and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            #    self.spaceship.shoot()
        
        is_key_pressed = pygame.key.get_pressed()
        if self.spaceship:
            if is_key_pressed[pygame.K_RIGHT]:
                self.spaceship.rotate(clockwise=True)
            elif is_key_pressed[pygame.K_LEFT]:
                self.spaceship.rotate(clockwise=False)
            if is_key_pressed[pygame.K_UP]:
                self.spaceship.accelerate()
            else:
                self.spaceship.decelerate()
            if is_key_pressed[pygame.K_SPACE]:
                current_time = pygame.time.get_ticks()
                if current_time - self.last_shot >= self.spaceship.shoot_delay:
                    self.last_shot = current_time
                    self.spaceship.shoot()
    
    def _process_game_logic(self):
        current_time = pygame.time.get_ticks()

        if self.active_upgrade and current_time >= self.upgrade_end_time:
            self.active_upgrade = None
            self.spaceship.reset_shoot_delay()
            self.spaceship.set_multishot(False)
        #expiration function
        if self.active_upgrade and current_time >= self.upgrade_end_time:
            self.active_upgrade = None
            self.spaceship.reset_shoot_delay()
            self.spaceship.set_multishot(False)

        for game_object in self._get_game_objects():
            game_object.move(self.screen)
        
        if self.spaceship:
            for asteroid in self.asteroids:
                if asteroid.collides_with(self.spaceship):
                    self.score += 10  # Increase the score
                    self.spaceship = None
                    self.message = "You lost!"
                    self.game_over()
                    return
        
        for bullet in self.bullets[:]:
            for asteroid in self.asteroids[:]:
                if asteroid.collides_with(bullet):
                    self.asteroids.remove(asteroid)
                    self.bullets.remove(bullet)
                    asteroid.split()
                    self.score += 50  # Increase score for hitting an asteroid
                    import random
                    if not self.upgrades and random.random() < 0.35: #10% chance
                        upgrade = Upgrade(asteroid.position)
                        self.upgrades.append(upgrade)
                    break

        #Collecting the power up
        if self.spaceship:
            for upgrade in self.upgrades[:]:
                if upgrade.collides_with(self.spaceship):
                    self.upgrades.remove(upgrade)
                    self.active_upgrade = upgrade.type
                    self.upgrade_end_time = current_time + upgrade.duration
                    if upgrade.type == "rapid_fire":
                        self.spaceship.set_shoot_delay(25) #higher RPM
                        self.spaceship.set_multishot(False)
                    elif upgrade.type == "multishot":
                        self.spaceship.set_shoot_delay(self.spaceship.DEFAULT_SHOOT_DELAY)
                        self.spaceship.set_multishot(True)
        
        for bullet in self.bullets[:]:
            if not self.screen.get_rect().collidepoint(bullet.position):
                self.bullets.remove(bullet)
        
        if not self.asteroids and self.spaceship:
            self.message = "You won!"
            self.game_over()
    
    def _draw(self):
        self.screen.blit(self.background, (0, 0))
        for game_object in self._get_game_objects():
            game_object.draw(self.screen)
        
        # Display the current score at the top-left corner
        print_text(self.screen, f"Score: {self.score}", self.font, (255, 255, 255), (15, 15))

        #show upgrade timer
        if self.active_upgrade:
            time_left = (self.upgrade_end_time - pygame.time.get_ticks()) // 1000
            print_text(self.screen, f"{self.active_upgrade.capitalize()}: {time_left}s", self.font, (255, 255, 255), (15,50))
        
        if self.message:
            print_text(self.screen, self.message, self.font)
        
        pygame.display.flip()
        self.clock.tick(60)
    
    def _get_game_objects(self):
        game_objects = [*self.asteroids, *self.bullets, *self.upgrades]
        if self.spaceship:
            game_objects.append(self.spaceship)
        return game_objects
    
    def game_over(self):
        get_player_name(self.font, self.screen, self.score)
        self.display_game_over()


    def display_game_over(self):
        """Show game over screen with restart option."""
        self.screen.fill((0, 0, 0))
        print_text(self.screen, "Game Over!", self.font, (255, 255, 255), (100, 300))
        print_text(self.screen, "Press R to Restart or Q to Quit", self.font, (255, 255, 255), (100, 350))
        pygame.display.flip()
        
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        main_menu(self.screen, self.font)
                        return
                    elif event.key == pygame.K_q:
                        self.running = False
                        pygame.quit()
                        return
