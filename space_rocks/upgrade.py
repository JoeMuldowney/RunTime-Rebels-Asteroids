# space_rocks/upgrade.py
import pygame
import random
from models import GameObject
from utils import load_sprite

class Upgrade(GameObject):
    def __init__(self, position, upgrade_type="rapid_fire"):
        self.type = random.choice(["rapid_fire", "multishot"])
        self.duration = 10000  # 10 seconds in milliseconds
        self.spawn_time = pygame.time.get_ticks()
        # Load and scale the sprite (e.g., to 20x20 pixels)
        if self.type == "rapid_fire":
            sprite_name = "rapid_icon"  # Rename if you have a specific rapid-fire sprite
        else:  # multishot
            sprite_name = "multishot_icon"
        original_sprite = load_sprite(sprite_name, True)
        scaled_sprite = pygame.transform.scale(original_sprite, (20, 20))  # Adjust size here
        GameObject.__init__(self, position, scaled_sprite, (0, 0))

    def move(self, surface):
        pass  # Upgrades don’t move, they float in place