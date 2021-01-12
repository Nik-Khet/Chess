import numpy as np
import os
import pygame


class board(object):
    def __init__(self):
        self.state = [[0,0,0,0,0,0,0,0] for i in range(8)]
        self.image = pygame.transform.scale(pygame.image.load(os.path.join('Assets','board.png')),(400,400))
        pass
    
    
    def printboard(self):
        print(self.state)
        pass
    def updateboard(self, mypiece):
        self.state[mypiece.get_pos()[0]][mypiece.get_pos()[1]]=mypiece
        
    
    def edit_state(self, piece):
        pass



class piece(object): 
    def __init__(self, row, col, colour, board):
        self.board = board
        self.row = row
        self.col = col
        self.colour = colour
        self.moves = []
        self.king = False
        self.board
        pass
    
    def __repr__(self):
        return 
    def get_pos(self):
        return self.col,self.row
    
    
class Queen(piece):
    def __init__(self, row, col, colour, board):
        super().__init__(row, col, colour, board)
        self.name = "Queen"
        self.image = pygame.transform.scale(pygame.image.load(os.path.join('Assets','queen_'+self.colour+'.png')),(50,50))

        pass
    def moves(self):
        x = self.col
        y = self.row
        chessboard = self.board.state
        moves = []

        #Vertically up
        valid=True
        count=0
        while valid:
            if count!=0:
                moves.append((x,y-count))
            count+=1
            if y-(count+1)<0:
                valid=False
            if chessboard[y][x]!=0:
                target_piece = chessboard[y][x]
                if target_piece.colour == self.colour:
                    valid=False

        #Vertically down
        valid=True
        count=0
        while valid:
            if count!=0:
                moves.append((x,y+count))
            count+=1
            if y+(count+1)>7:
                valid=False
            if chessboard[y][x]!=0:
                target_piece = chessboard[y][x]
                if target_piece.colour == self.colour:
                    valid=False
        
        #Horizontally Right

        return moves

