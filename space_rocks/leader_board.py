import csv
import os
import pygame
from utils import print_text
import pandas as pd

def save_score(name, score):
    """Save the player's score to a CSV file."""
    file_path = "scores.csv"
    file_exists = os.path.isfile(file_path)

    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Name", "Score"])
        writer.writerow([name, score])

def get_player_name(font, screen, score):
    background = pygame.image.load("./assets/sprites/displayscreen.png")
    """Prompt the player for their name."""
    name = ""
    input_active = True

    while input_active:
        screen.blit(background,(0,0))  # Black background
        print_text(screen, "Enter your name: " + name, font, (255, 255, 255), (100, 400))
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
    if not name:
        name = "Anonymous"
    save_score(name, score)

def load_top_scores(filename="scores.csv", top_n=5):
    df = pd.read_csv(filename)
    df = df.sort_values(by="Score", ascending=False)
    return df.head(top_n)

def show_leaderboard(screen, font):
    top_scores = load_top_scores()
    background = pygame.image.load("./assets/sprites/displayscreen.png")
    running = True
    while running:
        screen.blit(background,(0,0))
        print_text(screen, "Spaceships, Asteroids, Explosions", font, (255, 255, 255), (350, 25))
        print_text(screen, "All Time Top 5!", font, (255, 255, 0), (575, 100))

        for i, row in enumerate(top_scores.itertuples(), start=1):
            text = f"{i}. {row.Name} - {row.Score}"
            label = font.render(text, True, (255, 255, 255))
            screen.blit(label, (600, 225 + i * 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False  # Return to main menu