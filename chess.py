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

    def check_if_check(self, colour):
        whites_targets, blacks_targets = self.update_targets()
        for row in range(8):
            for col in range(8):
                if self.state[row][col] !=0:
                    if self.state[row][col].name == 'King':
                        if colour == 'w':
                            king_w = self.state[row][col]
                        elif colour == 'b':
                            king_b = self.state[row][col]
        if colour == 'w':
            if king_w.get_pos() in blacks_targets:
                return True
            else:
                return False
        if colour == 'b':
            if king_b.get_pos() in whites_targets:
                return True
            else:
                return False
        




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
    def print_info(self):
        piece_colour = 'white' if self.colour=='w' else 'black'
        print(self.name + ': ' + piece_colour+', moves: ' + str(self.moves) + ', attack moves: ' + str(self.attack_moves))

    def remove_illegal_moves(self):
        #Removes moves that would result in putting oneself in check
        i=0
        while i<len(self.attack_moves):
            test_board = board()
            test_board.state = self.board.state
            test_board.state[self.attack_moves[i][0]][self.attack_moves[i][1]] = self
            if test_board.check_if_check(self.colour):
                self.attack_moves.pop(i)
                i-=1
            i+=1
        i=0
        while i<len(self.moves):
            test_board = self.board
            test_board.state[self.moves[i][0]][self.moves[i][1]] = self
            if test_board.check_if_check(self.colour):
                self.moves.pop(i)
                i-=1
            i+=1


    

    
    
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