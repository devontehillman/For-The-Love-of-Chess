from enum import Enum 
from abc import ABC, abstractmethod

def Color(Enum):
    White = 0 
    Black = 1

class Piece(ABC):
    """
    
    Static Variables
        _game:list? Stores board? in order for the piece to keep track of the game.
        image:str Holds path to the image file
    """
    _game  = None
    image = "./images/pieces.png"

    def __init__(self, Color: Enum ):
        self.color = Color
        self._image = pygame.Surface((105, 105), pg.SRCALPHA)
    
    @property
    def color(self):
        return self._color
    
    def set_game(game):    
        if not isinstance(game, Game):        
            raise ValueError("You must provide a valid Game instance.")    
        Piece._game = game

    def set_image(self, x: int, y: int) -> None:
        """
        This code will take an x  and y  value and copy from our image file 
        a 105x105 pixel chunk into the current piece's image
        """
        self._image.blit(Piece.SPRITESHEET, (0, 0), pygame.rect.Rect(x, y, 105, 105))
    
    def inbounds(x,y):
        return (0 < y < 8) and (0 < x < 8)
    
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
        moves = []
    # For each step up until max distance
        for radius in range(0, distance):
            #Check spot at given radius 
            y = y + y_d
            x = x + x_d
            position_to_check = position_to_check[x][y]
            
            #Check if spot in bounds at given radius
            if not Piece.inbounds(x,y):
                return moves
            
            # No Piece at spot
            if self.board[x][y] == None:
                moves.append([x,y])
                continue
            
            #Theres a piece in spot check color
            #if same exit else add position and exit
            if self.color == position_to_check.color:
                exit
            else:
                moves.append([x,y])
                exit
            return moves
        

    def get_diagonal_moves(self, y: int, x: int, distance: int, moves) ->list[tuple[int, int]]:
        """
        These are convenience methods that simply call each directional method for all
        possible directions. 
        """
        moves += self._diagonal_moves(y, x, distance, 1, 1)
        moves += self._diagonal_moves(y, x, distance, -1, 1)
        moves += self._diagonal_moves(y, x, distance, 1, -1)
        moves += self._diagonal_moves(y, x, distance, -1, -1)
        return moves
    
    def _horizontal_moves(self, y: int, x: int, y_d: int, x_d: int, distance:int) -> list[tuple[int, int]]:
        """
        starts at a particular spot on the board, and
        find all valid moves in a given horizontal direction.
        """
        pass

    def get_horizontal_moves(self, y: int, x: int, distance: int) ->list[tuple[int, int]]:
        """
        These are convenience methods that simply call each of the previous methods for 
        all possible directions.

        """
        pass

    def _vertical_moves(self, y: int, x: int, y_d: int, x_d: int, distance:int) -> list[tuple[int, int]]:
        """
        starts at a particular spot on the board, and
        finds all valid moves in a given vertical direction.
        
        Returns:
            all valid moves in a given vertical direction.
        """
        pass


    def get_vertical_moves(self, y: int, x: int, distance: int) ->list[tuple[int, int]]:
        """
        These are convenience methods that simply call each of the previous methods for 
        all possible directions.

        """
        pass

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