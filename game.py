from piece_model import *

class stack():
        """
        holds prior board states to be utilized by redo/undo
        """
        def __init__(self):
            self.data = []
    
        def empty(self):
            return len(self.data) == 0 

        def push(self, info):
            return self.data.append(info)
        
        def peek(self):
            return self.data[-1]

        def pop(self):
            data = self.peek()
            del self.data[len(self.data) - 1]
            return data

class Game():

    def __init__(self):
        """
        setup the board and determine the current player
        """
        self._board = [[None for _ in range(8)] for _ in range(8)]
        self.current_player = Color.WHITE
        self._setup_pieces()

    
        
    def reset(self):
        """
        resets the board and pieces to default state
        """

    def _setup_pieces(self):
        """
        Initializes board by starting all pieces in their correct positions
        """
        self._board[0][0] = Rook(Color['BLACK'])
        self._board[0][1] = Knight(Color['BLACK'])
        self._board[0][2] = Bishop(Color['BLACK'])
        self._board[0][3] = Queen(Color['BLACK'])
        self._board[0][4] = King(Color['BLACK'])
        self._board[0][5] = Bishop(Color['BLACK'])
        self._board[0][6] = Knight(Color['BLACK'])
        self._board[0][7] = Rook(Color['BLACK'])
        
        
        for i in range(8):
            self._board[1][i] = Pawn(Color['BLACK'])
        
        self._board[7][0] = Rook(Color['WHITE'])
        self._board[7][1] = Knight(Color['WHITE'])
        self._board[7][2] = Bishop(Color['WHITE'])
        self._board[7][4] = Queen(Color['WHITE'])
        self._board[7][3] = King(Color['WHITE'])
        self._board[7][5] = Bishop(Color['WHITE'])
        self._board[7][6] = Knight(Color['WHITE'])
        self._board[7][7] = Rook(Color['WHITE'])
        
        
        for i in range(8):
            self._board[6][i] = Pawn(Color['WHITE'])



    def get(self, y:int, x:int):
        """
        Returns the piece at the given position or None if no piece exist
        Responsible for displaying pieces to board
        """
        return self._board[y][x]

    def switch_player(self):
        """
        Switches current player to opposing player
        """
        if self.Color == Color['WHITE']:
            self.Color = Color['BLACK']
        else:
            self.Color = Color['WHITE']

    def undo(self):
        """
        Pops the last board state from the stack and set the current board to it
        Return true if this can be done and false if there is no prior state
        """
        pass

    def copy_board(self):
        """
        allowing the human to undo a move, having a copy of the board allows 
        the AI to explore possible moves without affecting the current board. 
        Copying a board must be a deep copy - not a shallow copy. 
        """
        pass

    def move(self, piece: Piece, y: int, x: int, y2: int, x2: int) -> bool:
        """
        copy the board into the prior states stack then perform the move by setting 
        the new location to the piece, and removing the piece from the old location. 
        
        If the move was made by a Pawn , then the pawn should be
        updated to reflect that it is no longer the pawn's first move. 
        
        You must then determine if the
        move resulted in the current player being placed in check, and undo the move if it does.

        No player should be allowed to perform a move that places themselves in check.

        If the piece is a Pawn  and the new location is the opposite side of the board, the 
        pawn should be removed and a Queen  of the same color placed in its location.
        """
        pass
    
    def get_piece_locations(self, color: Color) -> list[tuple[int, int]]:
        """
        This will return the (y, x)  locations (as a tuple) for all the pieces on the board
        of the given color.
        """
        pass

    def find_king(self, color: Color) -> tuple[int, int]:
        """
        This will find the position of the King  of the given color.
        """
        _

    def check(self, color: Color) -> bool:
        """
        This method will get locations of the opposing pieces (use the method above). 
        It will then iterate over each of those pieces, calling their valid_moves  method, 
        and adding all valid moves for all pieces to a list of possible moves. The 
        method should then get the position of the king. If the positionof the king is in 
        the list of possible moves, the king is in check. Return True  in this case,
        and False  otherwise.
        """
        pass

    def _computer_move(self):
        """
        Implement a _computer_move  method that selects a random (but valid) move for the
        computer player. In the next phase, you will create a more robust method for picking
        computer moves.
        """
        pass
