from random import choice

class Bot:
    def __init__(self, app):
        self.app = app

    def generate_moves(self):
        valid_moves = {}

        # Check if there are pieces in the mid stack for the current player
        mid_stack_index = 1 if self.app.current_player == 'black' else 0
        if self.app.mid[mid_stack_index]:
            for piece in self.app.mid[mid_stack_index]:
                valid_moves_for_piece = self.generate_mid_stack_moves(piece)
                if valid_moves_for_piece:
                    valid_moves[-1] = valid_moves_for_piece  # Use -1 to indicate mid stack

        # If no pieces in mid stack or no valid moves from mid stack, check the rest of the board
        if not valid_moves:
            for point_index, stack in enumerate(self.app.points):
                if stack:
                    piece = stack[-1]
                    if piece.colour == self.app.current_player:
                        valid_moves[point_index] = self.dfs_moves(point_index, piece)

        return valid_moves

    def generate_mid_stack_moves(self, piece):
        valid_moves = []
        current_point_index = self.app.find_piece_point_index(piece)
        for dice_value in self.app.dice.get_current_face_values():
            new_point_index = current_point_index - dice_value
            if self.app.is_move_valid(piece, new_point_index):
                valid_moves.append(new_point_index)
        return valid_moves

    def dfs_moves(self, point_index: int, piece):
        valid_moves = []
        current_point_index = self.app.find_piece_point_index(piece)
        for dice_value in self.app.dice.get_current_face_values():
            new_point_index = current_point_index - dice_value
            if new_point_index < 0 and self.app.can_bear_off(piece.colour):
                new_point_index = -1  # Bear-off
            if self.app.is_move_valid(piece, new_point_index):
                valid_moves.append(new_point_index)
        return valid_moves

    def select_move(self):
        valid_moves = self.generate_moves()
        
        # Ensure valid_moves is not empty
        if not valid_moves:
            return None, None

        # Choose a point index with at least one valid move
        valid_point_indices = [point for point, moves in valid_moves.items() if moves]
        if not valid_point_indices:
            return None, None

        point_index = choice(valid_point_indices)
        moves = valid_moves[point_index]

        # Choose a move from the selected point index
        move = choice(moves)
        if point_index == -1:  # Mid stack move
            piece = self.app.mid[1 if self.app.current_player == 'black' else 0][-1]
        else:
            piece = self.app.points[point_index][-1]

        return piece, move