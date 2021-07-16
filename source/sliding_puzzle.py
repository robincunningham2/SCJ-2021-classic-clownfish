import random
from dataclasses import dataclass
from typing import List


def walk(string: str, step: int) -> str:
    """Helper generator to iterate over a string with steps"""
    for i in range(0, len(string), step):
        yield string[i:i+step]


def join(row: List[List[str]]) -> List[str]:
    """Join together a row of puzzle pieces into a complete list of lines"""
    res = []
    for i in range(len(row[0])):
        res.append('│')
        for piece in row:
            res[i] += piece[i]
    return res


def bordered(lines: List[str]) -> List[str]:
    """Put a border after every line"""
    return [line + '│' for line in lines]


@dataclass
class PiecePosition:
    """Position of a piece with its index"""

    x: int
    y: int
    index: int


class PuzzlePiece:
    """Piece of a bigger puzzle."""

    index: int

    width: int
    height: int

    __slots__ = ('index', 'width', 'height', '_data')

    def __init__(self, index: int, width: int, height: int) -> None:
        self.index = index

        self.width = width
        self.height = height

        self._data = []

    def __repr__(self) -> str:
        return f'<PuzzlePiece index={self.index} width={self.width} height={self.height} empty={self.empty}>'

    def __str__(self) -> str:
        return '\n'.join(self.data)

    def __bool__(self) -> bool:
        return bool(self._data)

    @property
    def data(self) -> List[str]:
        """List of lines of the image."""
        return self._data or [' ' * self.width] * self.height

    @property
    def empty(self) -> bool:
        """Whether this piece is empty (not filled)."""
        return not bool(self)

    def append(self, string: str) -> None:
        """Append a string to the end of the data list."""
        self._data.append(string)

    def clear(self) -> None:
        """Clear the piece data"""
        self._data = list()


class Puzzle:
    """Main puzzle game class, taking care of the whole game logic."""

    rows: List[List[PuzzlePiece]]

    __slots__ = ('rows',)

    def __init__(self, image: str, horizontal: int, vertical: int) -> None:
        """Initialize the Puzzle with an image and size to split it by.

        :param image: An ASCII string that will be split
        :param horizontal: Amount of horizontal rows
        :param vertical: Amount of vertical rows
        """
        data = image.split('\n')

        length = len(data[0])
        for line in data:
            if length != len(line):  # Make sure that all strings are equal in length
                raise ValueError('Image is not a complete rectangle, make sure it is correctly padded.')

        # How many characters one piece is
        width = len(data[0]) / horizontal
        height = len(data) / vertical

        # We cannot handle decimals
        if not width.is_integer():
            raise ValueError(f'Image cannot be evenly split by width: {len(data[0])} / {horizontal}')
        elif not height.is_integer():
            raise ValueError(f'Image cannot be evenly split by height: {len(data)} / {vertical}')

        # Even though width and height have no decimals, they are still floats
        width, height = int(width), int(height)

        rows: List[List[PuzzlePiece]] = [
            [
                # This will give each PuzzlePiece an index from 0 to (horizontal*vertical - 1)
                PuzzlePiece(i, width, height) for i in range(v*horizontal, v*horizontal+horizontal)
            ] for v in range(vertical)
        ]

        for i, line in enumerate(data):
            for j, column in enumerate(walk(line, width)):
                rows[i//height][j].append(column)

        self.rows = rows

    def __repr__(self) -> str:
        return f'<Puzzle solved={self.solved} rows={self.rows}>'

    @property
    def solved(self) -> bool:
        """Whether the puzzle is considered solved."""
        i = 0
        for row in self.rows:
            for piece in row:
                if piece.index != i:
                    return False

                i += 1
        return True

    def build_border(self, puzzle: int, piece: int, *, start: str, middle: str, end: str) -> str:
        """Build puzzle border line."""
        res = start + '─' * puzzle + end
        border_count = 1
        for i in range(piece, (puzzle - piece)):
            if i % piece == 0:
                pos = i + border_count
                res = res[:pos] + middle + res[pos + 1:]
                border_count += 1
        return res

    def draw(self) -> str:
        """Draw the puzzle in its current state."""
        nbr_separators = len(self.rows) - 1
        piece_width = self.rows[0][0].width
        puzzle_width = piece_width * len(self.rows[0]) + nbr_separators

        # build the top border
        output = [self.build_border(puzzle_width, piece_width, start='┌', middle='┬', end='┐')]

        # build content
        for index, row in enumerate(self.rows):
            row = [bordered(piece.data) for piece in row]
            output.extend(join(row))
            if index < len(self.rows) - 1:
                output.extend([self.build_border(puzzle_width, piece_width, start="├", middle="┼", end="┤")])

        # add bottom border
        output += [self.build_border(puzzle_width, piece_width, start='└', middle="┴", end='┘')]

        return '\n'.join(output)

    def shuffle(self) -> None:
        """Shuffle the puzzle by randomizing the order of the pieces"""
        for row in self.rows:
            random.shuffle(row)
        random.shuffle(self.rows)
        # Clear a random piece
        random.choice(random.choice(self.rows)).clear()

    def _get_empty_piece_position(self) -> PiecePosition:
        x, y, index = [
            (x, y, piece.index)
            for y, row in enumerate(self.rows)
            for x, piece in enumerate(row)
            if piece.empty
        ][0]
        return PiecePosition(x=x, y=y, index=index)

    def move_up(self) -> None:
        """Move the piece above the empty piece down"""
        empty_pos = self._get_empty_piece_position()
        # return if empty piece is on the first row
        if empty_pos.y == 0:
            return
        self._swap_pieces(x1=empty_pos.x, y1=empty_pos.y, x2=empty_pos.x, y2=empty_pos.y - 1)

    def move_down(self) -> None:
        """Move the piece below the empty piece up"""
        empty_pos = self._get_empty_piece_position()
        # return if empty piece is on the last row
        if empty_pos.y == len(self.rows) - 1:
            return
        # swap the empty piece with the target piece
        self._swap_pieces(x1=empty_pos.x, y1=empty_pos.y, x2=empty_pos.x, y2=empty_pos.y + 1)

    def move_right(self) -> None:
        """Move the piece at the right of the empty piece to the left"""
        empty_pos = self._get_empty_piece_position()
        # return if empty piece is on the last column
        if empty_pos.x == len(self.rows[0]) - 1:
            return
        self._swap_pieces(x1=empty_pos.x, y1=empty_pos.y, x2=empty_pos.x + 1, y2=empty_pos.y)

    def move_left(self) -> None:
        """Move the piece at the left of the empty piece to the right"""
        empty_pos = self._get_empty_piece_position()
        # return if empty piece is on the first column
        if empty_pos.x == 0:
            return
        # swap the empty piece with the target piece
        self._swap_pieces(x1=empty_pos.x, y1=empty_pos.y, x2=empty_pos.x - 1, y2=empty_pos.y)

    def _swap_pieces(self, x1: int, y1: int, x2: int, y2: int) -> None:
        self.rows[y1][x1], self.rows[y2][x2] = self.rows[y2][x2], self.rows[y1][x1]
