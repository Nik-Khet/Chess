import pygame

from chess import *

pygame.init()
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




black_checkmated = pygame.transform.scale(pygame.image.load(os.path.join('Assets','b_checkmated.png')),BOARD_SCALE)
white_checkmated = pygame.transform.scale(pygame.image.load(os.path.join('Assets','w_checkmated.png')),BOARD_SCALE)
stalemate        = pygame.transform.scale(pygame.image.load(os.path.join('Assets','stalemate.png')),BOARD_SCALE)


def convert_numpy_to_diplay(row_number, col_number):
    #Converts integer piece positions to pixel positions for display
    x = BOARD_POSITION[0] + col_number*BOARD_SCALE[0]/8
    y = BOARD_POSITION[1] + row_number*BOARD_SCALE[1]/8
    return x,y

def draw_window(chessboard):
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
    #Update display in case of checkmate
    if chessboard.checkmate:
        if chessboard.turn == 'w':
            DISPLAY.blit(white_checkmated, BOARD_POSITION)
        else:
            DISPLAY.blit(black_checkmated, BOARD_POSITION)
    if chessboard.stalemate:
        DISPLAY.blit(stalemate, BOARD_POSITION)
    pygame.display.update()
    
def setup_board():
    chessboard = board()
    chessboard.updateboard(King(7,3,'w',chessboard))
    chessboard.updateboard(Queen(7,4,'w',chessboard))
    chessboard.updateboard(Bishop(7,2,'w',chessboard))
    chessboard.updateboard(Bishop(7,5,'w',chessboard))
    chessboard.updateboard(Rook(7,0,'w',chessboard))
    chessboard.updateboard(Rook(7,7,'w',chessboard))
    for i in range(8):
        chessboard.updateboard(Pawn(6,i,'w',chessboard))
    
    chessboard.updateboard(King(0,3,'b',chessboard))
    chessboard.updateboard(Queen(0,4,'b',chessboard))
    chessboard.updateboard(Bishop(0,2,'b',chessboard))
    chessboard.updateboard(Bishop(0,5,'b',chessboard))
    chessboard.updateboard(Rook(0,0,'b',chessboard))
    chessboard.updateboard(Rook(0,7,'b',chessboard))
    for i in range(8):
        chessboard.updateboard(Pawn(1,i,'b',chessboard))
    
    return chessboard

def game_loop():
    run = True
    FPS=60
    clock = pygame.time.Clock()
    selected_piece = None
    chessboard = setup_board()
    
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            draw_window(chessboard)
            #Close Window
            if event.type == pygame.QUIT:
                run = False
            #If click
            if event.type == pygame.MOUSEBUTTONUP:
                #Print state of board
                for i in range(8):
                    print(chessboard.state[i])            

                #Convert click to row, col index
                x,y = pygame.mouse.get_pos()
                col_index = int((x-BOARD_POSITION[0])//(BOARD_SCALE[0]/8))
                row_index = int((y-BOARD_POSITION[1])//(BOARD_SCALE[1]/8))
                print(row_index,col_index)
                
                #Do standard move
                if selected_piece != None:
                    for i in chessboard.state[selected_piece[0]][selected_piece[1]].moves:
                        if i == (row_index,col_index):
                            chessboard.state[selected_piece[0]][selected_piece[1]].move(row_index,col_index)
                            chessboard.state[row_index][col_index].deselect()
                            selected_piece = None
                            chessboard.change_turn()
                
                #Do attacking move
                if selected_piece != None:
                    for i in chessboard.state[selected_piece[0]][selected_piece[1]].attack_moves:
                        if i == (row_index,col_index):
                            chessboard.state[selected_piece[0]][selected_piece[1]].move(row_index,col_index)
                            chessboard.state[row_index][col_index].deselect()
                            selected_piece = None
                            chessboard.change_turn()

                #Update moves for pieces and remove illegal (into check) moves for player whos turn it is
                chessboard.update_all_moves()
                for i in range(8):
                    for j in range(8):
                        if chessboard.state[i][j]!=0:
                            if chessboard.state[i][j].colour == chessboard.turn:
                                chessboard.state[i][j].remove_illegal_moves()

                #Deselect all pieces
                for i in range(8):
                    for j in range(8):
                        if chessboard.state[i][j] !=0:
                            if chessboard.state[i][j].selected:
                                chessboard.state[i][j].deselect()
                                selected_piece = None
                                
                #Select piece at click if it exists
                if chessboard.state[row_index][col_index] !=0:
                    if chessboard.state[row_index][col_index].colour == chessboard.turn:
                        chessboard.state[row_index][col_index].select()
                        selected_piece = [row_index,col_index]
                    else:
                        selected_piece=None

                #Check for checkmate
                chessboard.is_checkmate()
                
                #Print piece info
                print('Turn: '+chessboard.turn)
                for i in range(8):
                    for j in range(8):
                        if chessboard.state[i][j]!=0:
                            chessboard.state[i][j].print_info()
    pygame.quit()
        






def main():
    
    game_loop()
    
if __name__ == "__main__":
    main()