class Coordinate:
    def __init__(self, x: int = None, y: int = None) -> None:
        self.x = x
        self.y = y

class Box(Coordinate):
    def __init__(self, x: int = None, y: int = None, width: int = None, height: int = None) -> None:
        super().__init__(x, y)
        self.width = width
        self.height = height