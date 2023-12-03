from random import choice


class BackgammonBot:
    def __init__(self, app):
        self.app = app  # The App instance for accessing game state and methods

    def generate_moves(self):
        valid_moves = {}
        for point_index, stack in enumerate(self.app.points):
            if stack:
                piece = stack[-1]  # Get the top piece from the stack
                if piece.colour == self.app.current_player:
                    valid_moves[piece] = self.dfs_moves(point_index, piece)
        return valid_moves
    
    def dfs_moves(self, point_index, piece):
        valid_moves = []
        for dice_value in self.app.dice.get_current_face_values():
            new_point_index = self.calculate_new_point_index(point_index, dice_value, piece)
            if self.app.is_move_valid(piece, new_point_index):
                valid_moves.append(new_point_index)
        return valid_moves


    def calculate_new_point_index(self, point_index, dice_value, piece):
        if piece.colour == "white":
            return point_index + dice_value
        else:
            return point_index - dice_value

        
    def select_move(self):
        valid_moves = self.generate_moves()
        if valid_moves:
            piece, moves = choice(list(valid_moves.items()))
            move = choice(moves)
            print(piece, move)
            return piece, move
        return None, None