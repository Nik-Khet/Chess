import pygame
from chess import *

WIDTH= 900
HEIGHT = 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

def main():
    run = True
    FPS=60
    clock = pygame.time.Clock()
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()

if __name__ == "__main__":
    main()