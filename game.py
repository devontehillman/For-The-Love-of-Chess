import copy
import random
from piece_model import *


def inbounds(x, y):
    return (0 <= y < 8) and (0 <= x < 8)


class Stack():
    """
    holds prior board states to be utilized by redo/undo
    """

    def __init__(self):
        self.data = []

    def length(self):
        return len(self.data)

    def empty(self):
        return len(self.data) == 0

    def push(self, info):
        return self.data.append(info)

    def peek(self):
        return self.data[-1]

    def pop(self):
        # get the last element
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
        self.copy_board()

    def reset(self):
        """
        resets the board and pieces to default state
        """
        # clear prior moves
        while not self._B.empty():
            self._B.pop()

        # Create new board
        self._board = [[None for _ in range(8)] for _ in range(8)]

        # set up pieces on new board
        self._setup_pieces()

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

    def get(self, y: int, x: int) -> Piece:
        """
        Returns the piece at the given position or None if no piece exist
        Responsible for displaying pieces to board
        """
        # check if the position is on chess board and
        if inbounds(x, y) and isinstance(self._board[y][x], Piece):
            return self._board[y][x]
        else:
            return None

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
        if self._B.length() > 2 and (self._B.length() % 2) == 0 :
            self._B.pop()
            self._board = self._B.peek()
            return True
        if self._B.length() > 2 and (self._B.length() % 2) == 1 :
            self._B.pop()
            self._B.pop()
            self._board = self._B.peek()
            return True
        elif self._B.length() == 2:
            self._B.pop()
            self._board = self._B.peek()
        else:
            while not self._B.empty():
                self._B.pop()
                return False

    def copy_board(self):
        """
        allowing the human to undo a move, having a copy of the board allows
        the AI to explore possible moves without affecting the current board.
        Copying a board must be a deep copy - not a shallow copy.
        """
        self._prior = []
        self._prior = [[None for _ in range(8)] for _ in range(8)]
        for i in range(8):
            for j in range(8):
                piece = self._board[i][j]
                if piece is not None:
                    self._prior[i][j] = piece.copy()
                else:
                    self._prior[i][j] = None
        self._B.push(self._prior)
        print(self._B.length())

    def self_check_reset(self):
        self._board = self._B.peek()
        self._B.pop()
        self.copy_board()

    def move(self, piece: Piece, y: int, x: int, y2: int, x2: int) -> bool:
        """
        1. Copy the board into the prior states stack
        2. Then perform the move by setting the new location(y2,x2) to the piece,
        and removing the piece from the old location(y,x).
        #3 If the move was made by a Pawn , then the pawn should be
        updated to reflect that it is no longer the pawn's first move.
        #4 You must then determine if the move resulted in the current player
        being placed in check, and undo the move if it does.
        No player should be allowed to perform a move that places themselves in check.
        #5 If the piece is a Pawn  and the new location is the opposite side of the board, the
        pawn should be removed and a Queen  of the same color placed in its location.
        """
        # 1
        self.copy_board()
        # 2
        self._board[y][x] = None
        self._board[y2][x2] = piece
        # 3
        if isinstance(piece, Pawn):
            piece.first_move = False

        # 4 Check where king is and then for all opposing pieces check if its location is in their valid moves.
        # Essentially if you placed your self into check

        opposing_color = Color['BLACK']
        white = Color['WHITE']
        if self.check(white):
            self.self_check_reset()
            return False


        # 5 Is on the opposing side of the board
        # for white its opposing y2 == 0 and for black its opposing y2 == 7
        if isinstance(piece, Pawn):
            if piece.color == Color["WHITE"] and y2 == 0:
                self._board[y2][x2] = None
                self._board[y2][x2] = Queen(Color["WHITE"])
                return True
            elif piece.color == Color["BLACK"] and y2 == 7:
                self._board[y2][x2] = None
                self._board[y2][x2] = Queen(Color["BLACK"], self._board)
                return True

        return True

    def get_piece_locations(self, color: Color):
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

    def find_king(self, color: Color):
        """
        This will find the position of the King of the given color.
        """
        col = 0
        row_num = 0
        for row in self._board:
            for piece in row:
                if isinstance(piece, King) and piece._color == color:
                    return (row_num, col)
                col += 1
            row_num += 1
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
            row = piece[0]
            col = piece[1]
            # grab pice on board
            actual_piece = self._board[row][col]
            # find all of  its valid  moves
            total_opposing_team_moves += actual_piece.valid_moves(row, col)

        # Check if king is in
        if self.find_king(color) in total_opposing_team_moves:
            print("CHECK!")
            return True
        else:
            return False

    def _computer_move(self):
        """
        Implement a _computer_move  method that selects a random (but valid) move for the
        computer player. In the next phase, you will create a more robust method for picking
        computer moves.
        """
        # black automated movements
        color = Color['BLACK']
        # Gather all the location of the black pieces
        locations = self.get_piece_locations(color)

        moves = []
        while moves == []:
            # choose a random piece to move
            location = random.choice(locations)
            piece = self.get(location[0], location[1])
            # gather its possible moves
            moves = piece.valid_moves(location[0], location[1])
            # gather its possible moves
            moves = piece.valid_moves(location[0], location[1])
        # check if piece can move
        if moves != []:
            # choose a random move
            move = random.choice(moves)

        if self.move(piece, location[0], location[1], move[0], move[1]):
            return color.name + ' moved ' + str(
                type(piece).__name__) + "<br />"

        else:
            self.undo()
            self._computer_move()
    def mate(self, color: Color)-> bool:
        """
        Checkmate results when the king is in check and no moves left on the board will allow the 
        king to escape check. 
        To get out of check, the king can move, or another piece may move
        to block the piece threatening the king. 
        
        #1 First, call the check  method. If the king is not in check, the king
        cannot be in checkmate. 
        
        #2If the king is in check, you will then need to see if the king can
        escape. 
        #2.1You do this by getting a list of possible moves for the king, and a list of opponent
        pieces. 
        #2.2If there is a move the king can perform that is not in the list of the opponent's
        possible moves, the king is not in checkmate. 

        However, just because the king can't move to escape check doesn't immediately mean the king is in checkmate. 
        #3 If another piece can move such that it blocks the king being in check, then the king is safe. 
        
        To determine this, get a list of all possible moves for the current player. Loop through the list trying each
        move, and then calling the check method to see if that move resulted in check. If a move
        is found that results in the king not being in check, then the king is not in checkmate.
        Remember to undo each move after you test it.
        """
        #1
        if not self.check(color):
            return False

        #2.1
        #Gather who the opposing team is
        if color == Color['BLACK']:
            opposing_color = Color["WHITE"]
        else:
            opposing_color = Color['BLACK']
        
        #2.1get kings location and all possible moves
        king_pos = self.find_king(color)
        king = self.get(king_pos[0],king_pos[1])
        king_moves = king.valid_moves(king_pos[0], king_pos[1])
        #2.1 gather all opposing teams piece possible moves
        opposing_pieces = self.get_piece_locations(opposing_color)
        
        opposing_moves = []
        for piece_loc in opposing_pieces:
            piece = self.get(piece_loc[0], piece_loc[1])
            opposing_moves += piece.valid_moves(piece_loc[0], piece_loc[1])

        #2.2 Check if king can evade opposing team
        moves_that_threaten_king = []
        for move in king_moves:
            if move not in opposing_moves:
                return False
            else:
                moves_that_threaten_king.append(move)

        #3 Check to see if your other pieces can move to block opponent
        # Gather all of your pieces(the homies) and move them to see if you can get your king out of check 
        the_homies_loc = self.get_piece_locations(color)
        #loop to access all of your your team pieces with the gathered location        
        for homie_location in the_homies_loc:
            homie_moves = []
            homie = self.get(homie_location[0], homie_location[1])
            homie_moves += homie.valid_moves(piece[0], piece[1])
            #loop to check if any of the moves will get the king out of check
            for move in homie_moves:
                self.move(homie, homie_location[0], homie_location[1], move[0], move[1])
                #if the resulting move gets the king out of check then you can avoid check mate
                if self.check(color) == False:
                    self.undo()
                    return False
                #The move doesn't save king, but still undo move so board stays the same.
                self.undo()
        #If you get through all homies and can't be saved you are in check mate
        return True
            