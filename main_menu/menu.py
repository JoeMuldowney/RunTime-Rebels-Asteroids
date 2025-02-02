import pygame
from space_rocks.utils import print_text

def main_menu(screen, font):
    """ Display the main menu and wait for user input. """
    while True:
        screen.fill((0, 0, 0))  # Black background
        print_text(screen, "Game Name", font, (255, 255, 255),  (15,75))
        print_text(screen, "Press ENTER to Start", font, (255, 255, 255), (15, 125))
        print_text(screen, "Press ESC to Quit", font, (255, 255, 255), (15,175))
        print_text(screen, "Controls", font, (255, 255, 255), (15, 250))
        print_text(screen, "Spacebar to shoot", font, (255, 255, 255), (15, 300))
        print_text(screen, "Up arrow to move", font, (255, 255, 255), (15, 350))
        print_text(screen, "Left & right arrow to turn ship", font, (255, 255, 255), (15, 400))
        print_text(screen, "Settings", font, (255, 255, 255), (550, 75))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Start game
                    return
                if event.key == pygame.K_ESCAPE:  # Exit game
                    pygame.quit()
                    quit()