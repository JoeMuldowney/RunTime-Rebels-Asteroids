import pygame
from utils import print_text
from leader_board import show_leaderboard
def main_menu(screen, font):
    """ Display the main menu and wait for user input. """
    background = pygame.image.load("./assets/sprites/displayscreen.png")
    while True:
        screen.blit(background,(0,0))  # Black background
        print_text(screen, "Spaceships, Asteroids, Explosions", font, (255, 255, 255),  (5,25))
        print_text(screen, "Start (ENTER)", font, (255, 255, 255), (950, 125))
        print_text(screen, "Quit (ESC)", font, (255, 255, 255), (950,175))
        print_text(screen, "Leader Board (L)", font, (255, 255, 255), (950, 225))
        print_text(screen, "Controls", font, (255, 255, 255), (5, 650))
        print_text(screen, "Shoot (SPACE BAR)", font, (255, 255, 255), (5, 700))
        print_text(screen, "Move (UP ARROW)", font, (255, 255, 255), (5, 750))
        print_text(screen, "Turn (LEFT & RIGHT ARROW)", font, (255, 255, 255), (5, 800))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
                if event.key == pygame.K_l: # start game
                    show_leaderboard(screen, font)  # leaderboard screen
                if event.key == pygame.K_ESCAPE:  # Exit game
                    pygame.quit()
                    quit()