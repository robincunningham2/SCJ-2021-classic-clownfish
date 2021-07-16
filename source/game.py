from sliding_puzzle import Puzzle


class Game:
    """Game class"""

    def __init__(self, image: str, difficulty: int = 1):
        """Init function

        Args:
            image (str): image path
            difficulty (int, optional): integer ranging from 1 to 5. Defaults to 1.
        """
        difficulty = min(5, max(difficulty, 1))
        # Convert image to ASCII
        # self.ascii = toAscii(image)
        with open('../resources/ascii_art/amogus.txt', 'r') as f:
            self.ascii = f.read()
        # Need to adjust the dimensions for sliding_puzzle.Puzzle
        vertical = 0
        horizontal = 0
        self.puzzle = Puzzle(self.ascii, vertical, horizontal)
