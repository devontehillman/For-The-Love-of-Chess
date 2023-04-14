import copy
from piece_model import *

class Stack():
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
        self._B = Stack()

    
        
    def reset(self):
        """
        resets the board and pieces to default state
        """
        while not self._B.empty():
            self._B.pop()

    def _setup_pieces(self):
        """
        Initializes board by starting all pieces in their correct positions
        """
        self._board[0][0] = Rook(Color['BLACK'], self._board)
        self._board[0][1] = Knight(Color['BLACK'], self._board)
        self._board[0][2] = Bishop(Color['BLACK'], self._board)
        self._board[0][3] = Queen(Color['BLACK'], self._board)
        self._board[0][4] = King(Color['BLACK'], self._board)
        self._board[0][5] = Bishop(Color['BLACK'], self._board)
        self._board[0][6] = Knight(Color['BLACK'], self._board)
        self._board[0][7] = Rook(Color['BLACK'], self._board)
        
        
        for i in range(8):
            self._board[1][i] = Pawn(Color['BLACK'],  self._board)
        
        self._board[7][0] = Rook(Color['WHITE'], self._board)
        self._board[7][1] = Knight(Color['WHITE'], self._board)
        self._board[7][2] = Bishop(Color['WHITE'], self._board)
        self._board[7][4] = Queen(Color['WHITE'], self._board)
        self._board[7][3] = King(Color['WHITE'], self._board)
        self._board[7][5] = Bishop(Color['WHITE'], self._board)
        self._board[7][6] = Knight(Color['WHITE'], self._board)
        self._board[7][7] = Rook(Color['WHITE'], self._board)
        
        
        for i in range(8):
            self._board[6][i] = Pawn(Color['WHITE'], self._board)


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
        if self._B.empty():
            return False
        else:
            self._B.pop()
            self._board = self._B.peek()
            return True

    def copy_board(self):
        """
        allowing the human to undo a move, having a copy of the board allows 
        the AI to explore possible moves without affecting the current board. 
        Copying a board must be a deep copy - not a shallow copy. 
        """
        self._prior = copy.deepcopy(self._board)
        self._boardStack.push(self._prior)

    def move(self, piece: Piece, y: int, x: int, y2: int, x2: int) -> bool:
        """
        1. copy the board into the prior states stack 
        2. then perform the move by setting the new location(y2,x2) to the piece, 
        and removing the piece from the old location(y,x). 
        
        #3If the move was made by a Pawn , then the pawn should be
        updated to reflect that it is no longer the pawn's first move. 
        
        #4You must then determine if the move resulted in the current player 
        being placed in check, and undo the move if it does.

        No player should be allowed to perform a move that places themselves in check.

        #5 If the piece is a Pawn  and the new location is the opposite side of the board, the 
        pawn should be removed and a Queen  of the same color placed in its location.
        """
        #1 
        self._B.push(self._board)
        #2
        self._board[y][x] = None 
        self._board[y2][x2] = piece
        #3 pawn already takes care of this
        #4 Check where king is and then for all opposing pieces check if its location is in their valid moves. 
        #Essentially if you placed your self into check
        if self.check(piece.color):
            self.undo()
        

    
    def get_piece_locations(self, color: Color) -> list[tuple[int, int]]:
        """
        This will return the (y, x)  locations (as a tuple) for all the pieces on the board
        of the given color.
        """
        locations = []
        row = 0
        col = 0
        maxlength = 16 

        for y in self._board:
            for x in y:
                if x != None and x.color == color:
                    locations.append((row, col))
                    if len(locations) == maxlength:
                        return locations
                col += 1
            row += 1
            col = 0 

        return locations

    def find_king(self, color: Color) -> tuple[int, int]:
        """
        This will find the position of the King of the given color.
        """
        col  = 0 
        row_num = 0 
        for row in self._board:
            for piece in row:
                if isinstance(piece, King) and piece._color == color:
                        return (row_num, col)
                col += 1 
            rownum += 1
            col = 0

    def check(self, color: Color) -> bool:
        """
        This method will get locations of the opposing pieces (use the method above). 
        It will then iterate over each of those pieces, calling their valid_moves  method, 
        and adding all valid moves for all pieces to a list of possible moves. The 
        method should then get the position of the king. If the position of the king is in 
        the list of possible moves, the king is in check. Return True  in this case,
        and False  otherwise.
        """
        if color == Color['WHITE']:
            opposing_color = Color['BLACK']
        else:
            opposing_color = Color['WHITE']

        total_opposing_team_moves = []
        for piece in self.get_piece_locations(opposing_color):
            row =  piece[0]
            col =  piece[1]
            #grab pice on board
            actual_piece = self._board[row][col]
            #find all of  its valid  moves 
            total_opposing_team_moves += actual_piece.valid_moves(row,col)
        #Check if king is in
        if self.find_king(color) in total_opposing_team_moves:
            return True
        else:
            return False


    def _computer_move(self):
        """
        Implement a _computer_move  method that selects a random (but valid) move for the
        computer player. In the next phase, you will create a more robust method for picking
        computer moves.
        """
        color = Color['Black']
        locations = self.get_piece_locations(color)
        location = random.choice(locations)
        piece = self.get(location[0], location[1])
        moves = piece.valid_moves(location[0], location[1])
        move = random.choice(moves)
        
        if self.move(piece, location[0], location[1], move[0], move[1]):
            return

        else:
            self.undo()
            self._computer_move()
