import pygame

from chess import *
WIDTH= 900
HEIGHT = 500
DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")
WHITE = (255,255,255)
GREY = (200,200,200)
GREEN = (0,255,0)
RED = (255,0,0)
BOARD_POSITION = (250,50)
BOARD_SCALE = (400,400)

turn = 'w'

chessboard = board()
chessboard.updateboard(Queen(1,4,'w',chessboard))
chessboard.updateboard(Queen(3,4,'b',chessboard))
chessboard.updateboard(King(7,4,'b',chessboard))

def convert_numpy_to_diplay(row_number, col_number):
    #Converts integer piece positions to pixel positions for display
    x = BOARD_POSITION[0] + col_number*BOARD_SCALE[0]/8
    y = BOARD_POSITION[1] + row_number*BOARD_SCALE[1]/8
    return x,y

def draw_window():
    DISPLAY.fill(GREY)
    DISPLAY.blit(chessboard.image, BOARD_POSITION)
    #Update display to show pieces according to .state attribute of board object
    
    for row in range(8):
        for col in range(8):
            x,y = convert_numpy_to_diplay(row,col)
            if chessboard.board_colours[row][col]==1:
                pygame.draw.rect(DISPLAY,GREY,(x,y, BOARD_SCALE[0]/8, BOARD_SCALE[1]/8))
            if chessboard.board_colours[row][col]==2:
                pygame.draw.rect(DISPLAY,GREEN,(x,y, BOARD_SCALE[0]/8, BOARD_SCALE[1]/8))
            if chessboard.board_colours[row][col]==3:
                pygame.draw.rect(DISPLAY,RED,(x,y, BOARD_SCALE[0]/8, BOARD_SCALE[1]/8))

            if chessboard.state[row][col] != 0 :
                DISPLAY.blit(chessboard.state[row][col].image,(x,y))
    pygame.display.update()







def main():
    run = True
    FPS=60
    clock = pygame.time.Clock()
    
    selected_piece = None
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            draw_window()
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONUP:
                print(list(chessboard.board_colours))
                #Print state
                for i in range(8):
                    print(chessboard.state[i])            
                ###

                #Convert click to row, col index
                x,y = pygame.mouse.get_pos()
                col_index = int((x-BOARD_POSITION[0])//(BOARD_SCALE[0]/8))
                row_index = int((y-BOARD_POSITION[1])//(BOARD_SCALE[1]/8))
                print(row_index,col_index)

                if selected_piece != None:
                    for i in chessboard.state[selected_piece[0]][selected_piece[1]].moves:
                        if i == (row_index,col_index):
                            chessboard.state[selected_piece[0]][selected_piece[1]].move(row_index,col_index)
                            chessboard.state[row_index][col_index].deselect()
                            selected_piece = None
                            chessboard.change_turn()
                
                if selected_piece != None:
                    for i in chessboard.state[selected_piece[0]][selected_piece[1]].attack_moves:
                        if i == (row_index,col_index):
                            chessboard.state[selected_piece[0]][selected_piece[1]].move(row_index,col_index)
                            chessboard.state[row_index][col_index].deselect()
                            selected_piece = None
                            chessboard.change_turn()

                #Deselect all pieces
                for i in range(8):
                    for j in range(8):
                        if chessboard.state[i][j] !=0:
                            if chessboard.state[i][j].selected:
                                chessboard.state[i][j].deselect()
                                
                #Select piece at click if it exists
                if chessboard.state[row_index][col_index] !=0:
                    if chessboard.state[row_index][col_index].colour == chessboard.turn:
                        chessboard.state[row_index][col_index].select()
                        selected_piece = [row_index,col_index]
                    else:
                        selected_piece=None



                
                

    pygame.quit()
if __name__ == "__main__":
    main()