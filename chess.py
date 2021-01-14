import numpy as np
import os
import pygame
import copy

def other_colour(colour):
    if colour == 'w':
        return 'b'
    else:
        return 'w'

class board(object):
    def __init__(self):
        self.state = [[0,0,0,0,0,0,0,0] for i in range(8)]
        self.image = pygame.transform.scale(pygame.image.load(os.path.join('Assets','board.png')),(400,400))
        #Board_colours: 0=None, 1=grey, 2=green, 3=red
        self.board_colours = [[0,0,0,0,0,0,0,0] for i in range(8)]
        self.turn = 'w'
        self.checkmate=False
        pass
    
    
    def printboard(self):
        print(self.state)
        pass
    def updateboard(self, mypiece):
        self.state[mypiece.get_pos()[1]][mypiece.get_pos()[0]]=mypiece
    def remove_piece(self,row,col):
        self.state[row][col]=0
    
    def change_turn(self):
        if self.turn == 'w':
            self.turn = 'b'
        else:
            self.turn = 'w'
    
    def is_in_check(self, colour):
        if colour == 'w':
            enemy = 'b'
        else:
            enemy = 'w'
        for row in range(8):
            for col in range(8):
                if self.state[row][col]!=0:
                    if self.state[row][col].colour == colour and self.state[row][col].name == 'King':
                        king_pos = row,col
        for row in range(8):
            for col in range(8):
                if self.state[row][col]!=0:
                    if self.state[row][col].colour == enemy:
                        if king_pos in self.state[row][col].attack_moves:
                            return True
        return False

    def update_all_moves(self):
        #Runs update_moves for all pieces
        for i in range(8):
            for j in range(8):
                    if self.state[i][j]!=0:
                        self.state[i][j].update_moves()
    
    def update_colour_moves(self, colour):
        #Runs updates_moves for pieces of specific colour
        for i in range(8):
            for j in range(8):
                    if self.state[i][j]!=0 and self.state[i][j].colour == colour :
                        self.state[i][j].update_moves()
    
    def is_checkmate(self):
        #Counts total moves for player whos turn it is, if 0, turn on checkmate
        total_number_moves=0
        for i in range(8):
            for j in range(8):
                if self.state[i][j]!=0:
                    if self.state[i][j].colour==self.turn:
                        total_number_moves +=len(self.state[i][j].moves)+len(self.state[i][j].attack_moves)               
        if total_number_moves==0:
            self.checkmate=True
        else:
            self.checkmate=False
        print(self.checkmate)


    



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
        #prints name, colour, moves and attack_moves
        piece_colour = 'white' if self.colour=='w' else 'black'
        print(self.name + ': ' + piece_colour+', moves: ' + str(self.moves) + ', attack moves: ' + str(self.attack_moves))
    
    def select(self):
        #Selects piece on board and updates key (board_colours) for display
        #Board_colours: 0=None, 1=grey, 2=green, 3=red
        self.remove_illegal_moves()
        self.selected = True
        self.board.board_colours[self.row][self.col]=1
        for move in self.moves:
            self.board.board_colours[move[0]][move[1]]=2
        for move in self.attack_moves:
            self.board.board_colours[move[0]][move[1]]=3

    def deselect(self):
        self.board.board_colours = [[0,0,0,0,0,0,0,0] for i in range(8)]
        self.selected = False

    def remove_illegal_moves(self):
        #Removes moves that result in moving into check
        orig_row = self.row
        orig_col = self.col
        # for each move in self.moves
        # do move
        # update oppositions attack moves(and normal moves) 
        # if my king in check, remove move
        # undo move
        # re-update oppositions moves
        i=0
        while i<len(self.moves):
            self.move(self.moves[i][0],self.moves[i][1])
            self.board.update_colour_moves(other_colour(self.colour))
            if self.board.is_in_check(self.colour):
                self.moves.pop(i)
                i-=1
            self.move(orig_row,orig_col)
            
            i+=1
        i=0
        while i<len(self.attack_moves):
            piece_taken = self.board.state[self.attack_moves[i][0]][self.attack_moves[i][1]]
            self.move(self.attack_moves[i][0],self.attack_moves[i][1])
            self.board.update_colour_moves(other_colour(self.colour))
            restore_spot = self.attack_moves[i]
            if self.board.is_in_check(self.colour):
                self.attack_moves.pop(i)
                i-=1
            self.move(orig_row,orig_col)
            self.board.state[restore_spot[0]][restore_spot[1]]=piece_taken
            i+=1        
        self.board.update_colour_moves(other_colour(self.colour))
        print(self.board.state)
        return

    def move(self,row,col):

        old_row = self.row
        old_col = self.col
        self.row = row
        self.col = col
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
            if row+count>7:
                break
            if boardstate[row+count][col]!=0:
                if boardstate[row+count][col].colour == self.colour:
                    break
                else:
                    self.attack_moves.append((row+count, col))
                    break
        #Horizontally Right
        count=0
        while True:
            if count!=0:
                self.moves.append((row, col+count))
            count+=1
            if col+count>7:
                break
            if boardstate[row][col+count]!=0:
                if boardstate[row][col+count].colour == self.colour:
                    break
                else:
                    self.attack_moves.append((row, col+count))
                    break
        #Horizontally Left
        count=0
        while True:
            if count!=0:
                self.moves.append((row, col-count))
            count+=1
            if col-count<0:
                break
            if boardstate[row][col-count]!=0:
                if boardstate[row][col-count].colour == self.colour:
                    break
                else:
                    self.attack_moves.append((row, col-count))
                    break

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