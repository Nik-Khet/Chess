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
chessboard.updateboard(Queen(3,4,'w',chessboard))
chessboard.updateboard(Queen(1,4,'b',chessboard))


def convert_numpy_to_diplay(row_number, col_number):
    #Converts integer piece positions to pixel positions for display
    x = BOARD_POSITION[0] + col_number*BOARD_SCALE[0]/8
    y = BOARD_POSITION[1] + row_number*BOARD_SCALE[1]/8
    return x,y

def draw_window():
    WIN.fill(GREY)
    WIN.blit(chessboard.image, BOARD_POSITION)
    #Update display to show pieces according to .state attribute of board object
    for row in range(8):
        for col in range(8):
            if chessboard.state[row][col] != 0 :
                WIN.blit(chessboard.state[row][col].image,convert_numpy_to_diplay(row,col))
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
                #Print state
                ###
                for i in range(8):
                    print(chessboard.state[i])
                ###
                whites_targets = []
                blacks_targets = []
                for row in range(8):
                    for col in range(8):
                        if chessboard.state[row][col] != 0 :
                            if chessboard.state[row][col].colour == 'w':
                                whites_targets += chessboard.state[row][col].update_moves()[1]
                            if chessboard.state[row][col].colour == 'b':
                                blacks_targets += chessboard.state[row][col].update_moves()[1]
                            print(chessboard.state[row][col].name)
                

    pygame.quit()
if __name__ == "__main__":
    main()