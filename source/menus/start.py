import sys
from typing import TYPE_CHECKING, Union

from blessed import Terminal as Interface

from .utils import Menu, State

if TYPE_CHECKING:
    # Interface is a subclass of Terminal, importing it directly would cause circular imports
    from ..main import Interface  # noqa: F811

INSIDE_THE_BOX = [
    r'┌────────────────────────────────────────────────────────────────────────────────────────┐',
    r'│                                                                                        │',
    r'│         ___ _   _ ____ ___ ____  _____    _____ _   _ _____    ____   _____  __        │',
    r'│        |_ _| \ | / ___|_ _|  _ \| ____|  |_   _| | | | ____|  | __ ) / _ \ \/ /        │',
    r'│         | ||  \| \___ \| || | | |  _|      | | | |_| |  _|    |  _ \| | | \  /         │',
    r'│         | || |\  |___) | || |_| | |___     | | |  _  | |___   | |_) | |_| /  \         │',
    r'│        |___|_| \_|____/___|____/|_____|    |_| |_| |_|_____|  |____/ \___/_/\_\        │',
    r'│                                                                                        │',
    r'│                                                                                        │',
    r'└────────────────────────────────────────────────────────────────────────────────────────┘',
]


class StartMenu(Menu):
    """The start-menu for the game."""

    def __init__(self) -> None:
        self.selected = 0

    def render(self, term: Interface) -> str:
        """Render the start-menu."""
        rendered = term.move_y(term.height // 2 - 3)

        for line in INSIDE_THE_BOX:
            rendered += term.center(term.black_on_white(line) if self.selected == 0 else line) + '\n'

        rendered += term.move_y(term.height - 3)
        rendered += ' ' * 4 + (term.black_on_white('Exit') if self.selected == 1 else 'Exit')
        return rendered

    def kinput(self, term: Interface, key: Union[int, None]) -> None:
        """Handle keyboard input (what button is selected)."""
        if key in (term.KEY_UP, term.KEY_DOWN):
            self.selected = int(not self.selected)

    def click(self, term: Interface) -> State:
        """Handle a enter-press."""
        if self.selected == 0:
            return State.highscore
        else:
            sys.exit(0)
