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
        self.state[mypiece.get_pos()[1]][mypiece.get_pos()[0]]=mypiece
    def remove_piece(self,row,col):
        self.state[row][col]=0



class piece(object): 
    def __init__(self, row, col, colour, board):
        self.board = board
        self.row = row
        self.col = col
        self.colour = colour
        self.moves = []
        self.attack_moves = []
        self.king = False
        self.board
        pass
    
    def __repr__(self):
        return self.name+'_'+self.colour
    def get_pos(self):
        return self.col,self.row
    

    
    
class Queen(piece):
    def __init__(self, row, col, colour, board):
        super().__init__(row, col, colour, board)
        self.name = "Queen"
        self.image = pygame.transform.scale(pygame.image.load(os.path.join('Assets','queen_'+self.colour+'.png')),(50,50))
        pass

    def update_moves(self):
        self.moves = []
        self.attack_moves = []
        col = self.col
        row = self.row
        boardstate = self.board.state

        #Vertically up
        count=0
        while True:
            if count!=0:
                self.moves.append((row-count, col))
            count+=1
            if row-count<0:
                break
            if boardstate[row-count][col]!=0:
                if boardstate[row-count][col].colour == self.colour:
                    break
                else:
                    self.attack_moves.append((row-count, col))
                    break
        #Vertically down
        #Horizontally Right

        return self.moves, self.attack_moves

class King(piece):
    def __init__(self, row, col, colour, board):
        super().__init__(row, col, colour, board)
        self.name = "King"
        self.king = True
        self.image = pygame.transform.scale(pygame.image.load(os.path.join('Assets','queen_'+self.colour+'.png')),(50,50))
        pass

    def update_moves(self):
        self.moves = []
        self.attack_moves = []
        col = self.col
        row = self.row
        boardstate = self.board.state
        #Vertically up
        #Vertically down
        #Horizontally Right
        return self.moves, self.attack_moves