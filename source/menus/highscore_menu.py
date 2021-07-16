from typing import TYPE_CHECKING, Union

from blessed import Terminal as Interface
from highscore import Highscore

from .utils import Menu, State, set_string_length

if TYPE_CHECKING:
    # Interface is a subclass of Terminal, importing it directly would cause circular imports
    from ..main import Interface  # noqa: F811


class HighScoreMenu(Menu):
    """The highscore menu."""

    def __init__(self):
        self.selected = 0

        self.puzzles = Highscore().highscore

    def render(self, term: Interface) -> str:
        """Render the highscore table and a button to add new highscore."""
        rendered = ''

        rendered += (
            '    ' + set_string_length('Puzzle Name', term.width - 52)
            + '   ' + 'Player Name     '
            + '  ' + 'Highscore                  '
        ) + '\n\n'

        for i, puzzle in enumerate(self.puzzles):

            line = '    '
            line += set_string_length(puzzle['Puzzle'], term.width - 52) + '   '
            line += set_string_length(puzzle['Name'], 16) + '  '
            line += set_string_length(str(puzzle['Time']) + ' Seconds / ' + str(puzzle['Moves']) + ' Moves', 27)
            rendered += term.black_on_white(line) if self.selected == i else line
            rendered += '\n'

        rendered += term.move_y(term.height - 3)
        rendered += ' ' * 4 + (term.black_on_white('Add new') if self.selected == len(self.puzzles) else 'Add new')
        return rendered

    def click(self, term: Interface) -> State:
        """Handle enter key presses, changing state to file_explorer if the Add new button is selected."""
        if self.selected != len(self.puzzles):
            return State.highscore  # Don't change menu

        return State.file_explorer

    def kinput(self, term: Interface, key: Union[int, None]) -> None:
        """Handle arrow key input, changing the selected button."""
        if key == term.KEY_UP:
            self.selected -= 1
        elif key == term.KEY_DOWN:
            self.selected += 1

        # Clamp the value
        self.selected = max(0, min(self.selected, len(self.puzzles)))
