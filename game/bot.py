from random import choice


class Bot:
    def __init__(self, app):
        self.app = app  # The App instance for accessing game state and methods

    def generate_moves(self):
        valid_moves = {}
        for point_index, stack in enumerate(self.app.points):
            if stack:
                piece = stack[-1]  # Get the top piece from the stack
                if piece.colour == self.app.current_player:
                    valid_moves[point_index] = self.dfs_moves(point_index, piece)
        return valid_moves
    
    def dfs_moves(self, point_index: int, piece):
        valid_moves = []
        current_point_index = self.app.find_piece_point_index(piece)
        
        for dice_value in self.app.dice.get_current_face_values():
            # Calculate new point index for white pieces
            new_point_index = current_point_index - dice_value
            
            # Handle bearing off
            if new_point_index < 0:
                if self.app.can_bear_off(piece.colour):
                    new_point_index = -1  # Use -1 to indicate bearing off

            # Validate the move
            if self.app.is_move_valid(piece, new_point_index):
                valid_moves.append(new_point_index)

        return valid_moves

    def select_move(self):
        valid_moves = self.generate_moves()
        
        # Filter out points that do not have any valid moves
        valid_moves = {point: moves for point, moves in valid_moves.items() if moves}

        # Check if there are any points with valid moves
        if valid_moves:
            point_index, moves = choice(list(valid_moves.items()))
            move = choice(moves)
            piece = self.app.points[point_index][-1]  # Get the top piece from the stack at point_index
            return piece, move

        # Return None, None if there are no points with valid moves
        return None, None

