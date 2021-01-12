import pygame

from chess import *
WIDTH= 900
HEIGHT = 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")
WHITE = (255,255,255)
GREY = (200,200,200)
BOARD_POSITION = (250,50)
BOARD_SCALE = (400,400)

chessboard = board()
#chessboard.state[0][0] = Queen(0,0,'w',chessboard)
chessboard.updateboard(Queen(0,4,'w',chessboard))


def convert_numpy_to_diplay(row_number, col_number):
    x = BOARD_POSITION[0] + col_number*50
    y = BOARD_POSITION[1] + row_number*50
    return x,y

def draw_window():
    WIN.fill(GREY)
    WIN.blit(chessboard.image, BOARD_POSITION)
    for j in range(8):
        for i in range(8):
            if chessboard.state[j][i] != 0 :
                WIN.blit(chessboard.state[j][i].image,convert_numpy_to_diplay(j,i))



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