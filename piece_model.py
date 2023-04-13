from enum import Enum 
from abc import ABC, abstractmethod
import pygame 
import copy

class Color(Enum):
    WHITE = 0 
    BLACK = 1

class Piece(ABC):
    """
    
    Static Variables
        _game:list? Stores board? in order for the piece to keep track of the game.
        image:str Holds path to the image file
    """
    _game  = []
    SPRITESHEET =  pygame.image.load("./images/pieces.png")

    def __init__(self, color: Color, board):
        self._color = color
        self._image = pygame.Surface((105, 105), pygame.SRCALPHA)
        self._board = board

    @property
    def color(self):
        return self._color
    
    #Should I delete?
    @color.setter
    def color(self, val):
        self.color == val
    
    def set_game(game):    
        if not isinstance(game, Game):        
            raise ValueError("You must provide a valid Game instance.")    
        Piece._game = game

    def set_image(self, y: int, x: int) -> None:
        """
        This code will take an x  and y  value and copy from our image file 
        a 105x105 pixel chunk into the current piece's image
        """
        self._image.blit(Piece.SPRITESHEET, (0,0), pygame.rect.Rect(y*105, x*105, 105, 105))
    
    def inbounds(x,y):
        return (0 <= y < 8) and (0 <= x < 8)
    
    def _diagonal_moves(self, y: int, x: int, y_d: int, x_d: int, distance:int) -> list[tuple[int, int]]:
        """
        starts at a particular spot on the board, and
        find all valid moves in a given diagonal direction. 
        
        Params:
            y: int, x: int Board position of piece
                y: int vertical position 0 is top 7 is bottom spot
                x: int horizontal position 0 is left 7 is right most spot
            y_d: int, x_d: int Direction Vector
                y_d: int: vertical direction where -1 is up and 1 is down
                x_d: int: horizontal direction where -1 is left and 1 is right
            distance: How far the piece can move in a given direction
        Returns:
            List of possible positions the pice can move to
        """
        row = y
        col = x
        moves = []
    # For each step up until max distance
        for radius in range(0, distance):
            #Check spot at given radius 
            row = row + y_d
            col = col + x_d
            
            #Check if spot in bounds at given radius
            if not Piece.inbounds(row,col):
                return moves
            
            position_to_check = self.board[row][col]
            
            # No Piece at spot
            if self.board[row][col] == None:
                moves.append((row,col))
                continue
            
            #Theres a piece in spot check color
            #if same exit else add position and exit
            if self.color == position_to_check.color:
                exit
            else:
                moves.append((row,col))
                exit
        return moves

    def get_diagonal_moves(self, y: int, x: int, distance: int) ->list[tuple[int, int]]:
        """
        These are convenience methods that simply call each directional method for all
        possible directions. 
        """
        moves = []
        # Down to the right 
        moves += self._diagonal_moves(y, x, 1, 1, distance)
        #Up to the right
        moves += self._diagonal_moves(y, x, -1, 1, distance)
        #Down to the left
        moves += self._diagonal_moves(y, x, 1, -1, distance)
        #Up to the left 
        moves += self._diagonal_moves(y, x, -1, -1, distance)
        return moves
    
    def _horizontal_moves(self, y: int, x: int, y_d: int, x_d: int, distance:int) -> list[tuple[int, int]]:
        """
        starts at a particular spot on the board, and
        find all valid moves in a given horizontal direction.
        """
        row = y
        col = x
        moves = []
        # For each step up until max distance
        for radius in range(0, distance):
            #Check spot at given radius 
            col = col + x_d
            
            #Check if spot in bounds at given radius
            if not Piece.inbounds(row,col):
                return moves
            
            position_to_check = self.board[row][col]
            # No Piece at spot
            if self.board[row][col] == None:
                moves.append((row,col))
                continue
            
            #Theres a piece in spot check color
            #if same exit else add position and exit
            if self.color == position_to_check.color:
                exit
            else:
                moves.append((row,col))
                exit
            return moves

    def get_horizontal_moves(self, y: int, x: int, distance: int) ->list[tuple[int, int]]:
        """
        These are convenience methods that simply call each of the previous methods for 
        all possible directions.

        """
        moves = []
        #check right
        moves += self._horizontal_moves(y, x, 0, 1, distance)
        #check left 
        moves += self._horizontal_moves(y, x, 0, -1, distance)
        return moves

    def _vertical_moves(self, y: int, x: int, y_d: int, x_d: int, distance:int) -> list[tuple[int, int]]:
        """
        starts at a particular spot on the board, and
        finds all valid moves in a given vertical direction.
        
        Returns:
            all valid moves in a given vertical direction.
        """
        row = y
        col = x
        moves = []
        # For each step up until max distance
        for radius in range(0, distance):
            #Check spot at given radius 
            row = row + y_d
            x = col
            
            #Check if spot in bounds at given radius
            if not Piece.inbounds(row,col):
                return moves
            
            position_to_check = self._board[row][col]
            
            # No Piece at spot
            if self._board[row][col] == None:
                moves.append((row,col))
                continue
            
            #Theres a piece in spot check color
            #if same exit else add position and exit
            if self.color == position_to_check.color:
                exit
            else:
                moves.append((row,col))
                exit
        return moves

    def get_vertical_moves(self, y: int, x: int, distance: int) ->list[tuple[int, int]]:
        """
        These are convenience methods that simply call each of the previous methods for 
        all possible directions.
        """
        moves = []
        # check down 
        moves += self._vertical_moves(y, x, 1, 0, distance)
        # check up
        moves += self._vertical_moves(y, x, -1, 0, distance)
        return moves

    @abstractmethod
    def valid_moves(self, y: int, x: int) -> list[tuple[int, int]]:
        """
        This function will determine all valid moves for a piece at the given location.
        This is accomplished by calling the appropriate direction checking functions
        """
        pass
    
    def copied(self):
        """
        This function will copy a piece. We will use this to simulate
        possible moves for the computer, by copying the state of the board (and thus the
        pieces)
        """
        pass

class King(Piece):
    def __init__(self, color, board):
        super().__init__(color, board)
        self.color = color
        self.board = board

        if self.color == Color['WHITE']:
            self.set_image(0,0)
        
        if self.color == Color['BLACK']:
            self.set_image(0,1)
    
    def valid_moves(self, y: int, x: int) -> list[tuple[int, int]]:
        moves = [(y,x)]
        moves += super().get_horizontal_moves(y, x, 1)
        moves += super().get_vertical_moves(y, x, 1)
        moves += super().get_diagonal_moves(y, x, 1)

        return moves
    
    def copied(self):
        return copy.deepcopy(self) #is this what I am supposed to do?

class Queen(Piece):
    def __init__(self, color, board):
        super().__init__(color, board)
        self.color = color
        self.board = board

        if self.color == Color['WHITE']:
            self.set_image(1,0)

        if self.color == Color['BLACK']:
            self.set_image(1,1)
    
    def valid_moves(self, y: int, x: int) -> list[tuple[int, int]]:
        moves = [(y,x)]
        moves += super().get_horizontal_moves(y, x, 8)
        moves += super().get_vertical_moves(y, x, 8)
        moves += super().get_diagonal_moves(y, x, 8)

        return moves
    
    def copied():
        return copy.deepcopy(self) #is this what I am supposed to do?
    
class Bishop(Piece):
    def __init__(self, color, board):
        super().__init__(color, board)
        self.color = color
        self.board = board

        if self.color == Color['WHITE']:
            self.set_image(2,0)

        if self.color == Color['BLACK']:
            self.set_image(2,1)
    
    def valid_moves(self, y: int, x: int) -> list[tuple[int, int]]:
        moves = [(y,x)]
        moves += super().get_diagonal_moves(y, x, 8)

        return moves
    
    def copied(self):
        return copy.deepcopy(self) #is this what I am supposed to do?
    
class Knight(Piece):
    def __init__(self, color, board):
        super().__init__(color, board)
        self.color = color
        self.board = board

        if self.color == Color['WHITE']:
            self.set_image(3,0)

        if self.color == Color['BLACK']:
            self.set_image(3,1)

    def valid_moves(self, y, x):
        moves = [(y,x)]
        possible_moves = [(y+2, x+1), (y+2, x-1), (y+1, x+2), (y+1, x-2),
                            (y-2, x+1), (y-2, x-1), (y-1, x+2), (y-1, x-2)]
        for move in possible_moves:
            if 0 <= move[0] <= 8 and 0 <= move[1] <= 8:
                if self.board[move[0]][move[1]] != self.color:
                    moves.append(move)

        return moves
    
    def copied(self):
        return copy.deepcopy(self) #is this what I am supposed to do?

class Rook(Piece):
    def __init__(self, color, board):
        super().__init__(color, board)
        self.color = color
        self.board = board

        if self.color == Color['WHITE']:
            self.set_image(4,0)

        if self.color == Color['BLACK']:
            self.set_image(4,1)
    
    def valid_moves(self, y: int, x: int) -> list[tuple[int, int]]:
        moves = [(y,x)]
        moves += super().get_horizontal_moves(y, x, 8)
        moves += super().get_vertical_moves(y, x, 8)

        return moves
    
    def copied():
        return copy.deepcopy(self) #is this what I am supposed to do?
    
class Pawn(Piece):
    def __init__(self, color, board):
        super().__init__(color, board)
        self.color = color
        self.first_move = True
        self.board = board

        if self.color == Color['WHITE']:
            self.set_image(5,0)

        if self.color == Color['BLACK']:
            self.set_image(5,1)

    def valid_moves(self, y, x):
        moves = [(y,x)]
        if not self.first_move:
            moves += super().get_vertical_moves(y, x, 2)
            self.first_move = True

        if self.first_move:
            moves += super().get_vertical_moves(y, x, 1)

        possible_piece_right = self.board[y+1][x+1]
        if possible_piece_right != self.color and possible_piece_right is not None:
            moves += possible_piece_right

        possible_piece_left = self.board[y+1][x-1]
        if possible_piece_left != self.color and possible_piece_left is not None:
            moves += possible_piece_left

        return moves
    
    def copy(self):
        return copy.deepcopy(self)
