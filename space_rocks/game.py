import pygame
import csv
import os
import sys
from utils import get_random_position, load_sprite, print_text
from models import Asteroid, Spaceship

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from main_menu.menu import main_menu

class SpaceRocks:
    MIN_ASTEROID_DISTANCE = 250
    
    def __init__(self):
        self._init_pygame()
        self.screen = pygame.display.set_mode((1550, 900))
        self.background = load_sprite("space", False)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 64)
        self.message = ""
        self.asteroids = []
        self.bullets = []
        self.score = 0  # Initializing score
        self.spaceship = Spaceship((400, 300), self.bullets.append)
        
        for _ in range(6):
            while True:
                position = get_random_position(self.screen)
                if position.distance_to(self.spaceship.position) > self.MIN_ASTEROID_DISTANCE:
                    break
            self.asteroids.append(Asteroid(position, self.asteroids.append))

    def main_loop(self):
        main_menu(self.screen, self.font)  # Call the menu function
        while True:
            self._handle_input()
            self._process_game_logic()
            self._draw()
    
    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Space Rocks")
    
    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                quit()
            elif self.spaceship and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.spaceship.shoot()
        
        is_key_pressed = pygame.key.get_pressed()
        if self.spaceship:
            if is_key_pressed[pygame.K_RIGHT]:
                self.spaceship.rotate(clockwise=True)
            elif is_key_pressed[pygame.K_LEFT]:
                self.spaceship.rotate(clockwise=False)
            if is_key_pressed[pygame.K_UP]:
                self.spaceship.accelerate()
    
    def _process_game_logic(self):
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
                    break
        
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
        
        if self.message:
            print_text(self.screen, self.message, self.font)
        
        pygame.display.flip()
        self.clock.tick(60)
    
    def _get_game_objects(self):
        game_objects = [*self.asteroids, *self.bullets]
        if self.spaceship:
            game_objects.append(self.spaceship)
        return game_objects
    
    def game_over(self):
        player_name = self.get_player_name()
        self.save_score(player_name, self.score)
        self.display_game_over()
    
    def get_player_name(self):
        """Prompt the player for their name."""
        name = ""
        input_active = True
        
        while input_active:
            self.screen.fill((0, 0, 0))
            print_text(self.screen, "Enter your name: " + name, self.font, (255, 255, 255), (100, 400))
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return "Anonymous"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        name += event.unicode
        
        return name if name else "Anonymous"
    
    def save_score(self, name, score):
        """Save the player's score to a CSV file."""
        file_path = "scores.csv"
        file_exists = os.path.isfile(file_path)
        
        with open(file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["Name", "Score"])
            writer.writerow([name, score])
    
    def display_game_over(self):
        """Show game over screen with restart option."""
        self.screen.fill((0, 0, 0))
        print_text(self.screen, "Game Over!", self.font, (255, 255, 255), (100, 300))
        print_text(self.screen, "Press R to Restart or Q to Quit", self.font, (255, 255, 255), (100, 350))
        pygame.display.flip()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        main_menu(self.screen, self.font)
                        return
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        return
