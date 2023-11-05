class BackgammonBoard:
    def __init__(self):
        self.points = [[] for _ in range(24)]  # 24 points on the board

    def add_piece(self, point, piece):
        self.points[point].append(piece)

    def remove_piece(self, point):
        return self.points[point].pop() if self.points[point] else None

    def move_piece(self, start_point, end_point):
        # TODO: Implement moving a piece from one point to another