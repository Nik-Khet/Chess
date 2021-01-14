import numpy as np
import os
import pygame


class board(object):
    def __init__(self):
        self.state = [[0,0,0,0,0,0,0,0] for i in range(8)]
        self.image = pygame.transform.scale(pygame.image.load(os.path.join('Assets','board.png')),(400,400))
        #Board_colours: 0=None, 1=grey, 2=green, 3=red
        self.board_colours = [[0,0,0,0,0,0,0,0] for i in range(8)]
        self.turn = 'w'
        pass
    
    
    def printboard(self):
        print(self.state)
        pass
    def updateboard(self, mypiece):
        self.state[mypiece.get_pos()[1]][mypiece.get_pos()[0]]=mypiece
    def remove_piece(self,row,col):
        self.state[row][col]=0
    
    def update_targets(self):
        whites_targets = []
        whites_moves = []
        blacks_targets = []
        blacks_moves = []
        for row in range(8):
            for col in range(8):
                if self.state[row][col] != 0 :
                    if self.state[row][col].colour == 'w':
                        whites_targets += self.state[row][col].update_moves()[1]
                    if self.state[row][col].colour == 'b':
                        blacks_targets += self.state[row][col].update_moves()[1]
        return whites_targets, blacks_targets

    def change_turn(self):
        if self.turn == 'w':
            self.turn = 'b'
        else:
            self.turn = 'w'

class piece(object): 
    def __init__(self, row, col, colour, board):
        self.board = board
        self.row = row
        self.col = col
        self.colour = colour
        self.moves = []
        self.attack_moves = []
        self.king = False
        self.selected = False
        pass
    
    def __repr__(self):
        return self.name+'_'+self.colour
    
    def get_pos(self):
        return self.col,self.row
    
    def print_info(self):
        piece_colour = 'white' if self.colour=='w' else 'black'
        print(self.name + ': ' + piece_colour+', moves: ' + str(self.moves) + ', attack moves: ' + str(self.attack_moves))
    
    def select(self):
        #Board_colours: 0=None, 1=grey, 2=green, 3=red
        self.selected = True
        self.board.board_colours[self.row][self.col]=1
        self.update_moves()
        for move in self.moves:
            self.board.board_colours[move[0]][move[1]]=2
        for move in self.attack_moves:
            self.board.board_colours[move[0]][move[1]]=3

    def deselect(self):
        self.board.board_colours = [[0,0,0,0,0,0,0,0] for i in range(8)]
        self.selected = False

    def remove_illegal_moves(self):
        pass

    def move(self,row,col):
        old_row = self.row
        old_col = self.col
        self.row = row
        self.col = col
        self.board.state[row][col] = 0
        print(self.board.state)
        self.board.state[row][col] = self
        self.board.state[old_row][old_col] = 0
        pass

    

    

    
    
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
        count=0
        while True:
            if count!=0:
                self.moves.append((row+count, col))
            count+=1
            if row-+count>7:
                break
            if boardstate[row+count][col]!=0:
                if boardstate[row+count][col].colour == self.colour:
                    break
                else:
                    self.attack_moves.append((row+count, col))
                    break

        #Horizontally Right

        self.remove_illegal_moves()
        return self.moves, self.attack_moves

class King(piece):
    def __init__(self, row, col, colour, board):
        super().__init__(row, col, colour, board)
        self.name = "King"
        self.king = True
        self.image = pygame.transform.scale(pygame.image.load(os.path.join('Assets','pawn_'+self.colour+'.png')),(50,50))
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