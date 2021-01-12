import pygame

from chess import *
WIDTH= 900
HEIGHT = 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")
WHITE = (255,255,255)

chessboard = board()
def draw_window():
    #WIN.fill(WHITE)
    WIN.blit(chessboard.image, (300,100))
    pygame.display.update()


def main():
    run = True
    FPS=60
    clock = pygame.time.Clock()
    


    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            draw_window()
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                print(pos)
                

    pygame.quit()

if __name__ == "__main__":
    main()