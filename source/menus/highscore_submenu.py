from typing import TYPE_CHECKING

from blessed import Terminal as Interface
from game import Game
from highscore import Highscore

from .utils import Menu, set_string_length

if TYPE_CHECKING:
    # Interface is a subclass of Terminal, importing it directly would cause circular imports
    from ..main import Interface  # noqa: F811


class HighScoreSubMenu(Menu):
    """The highscore sub-menu."""

    def __init__(self, puzzle: str) -> None:
        self.selected = 0
        self.puzzle = puzzle
        self.highscores = []
        highscores = Highscore().highscore

        for hs in highscores:
            if hs['Puzzle'] == self.puzzle and hs not in self.highscores:
                self.highscores.append(hs)

        self.highscores.sort(key=lambda x: x['Moves'] + x['Time'])

    def render(self, term: Interface) -> str:
        """Render the highscores."""
        rendered = []
        rendered.append(term.move_down(1))
        for i, highscore in enumerate(self.highscores):
            color = term.webgrey
            if i == 0:
                color = term.color_rgb(215, 190, 105)
            if i == 1:
                color = term.color_rgb(192, 192, 192)
            if i == 2:
                color = term.color_rgb(169, 113, 66)

            rendered.append(
                term.move_x(4)
                + color(set_string_length(f'{i + 1}. {highscore["Name"]}', term.width - 36))
                + f'{highscore["Moves"]} moves / {highscore["Time"]} seconds'
            )

        rendered.append(term.move_yx(term.height - 3, 4) + 'Press enter to play this puzzle')
        return '\n'.join(rendered)

    def click(self, term: Interface) -> Menu:
        """Handle enter key presses."""
        return Game(self.puzzle)  # TODO: fetch puzzle from name
