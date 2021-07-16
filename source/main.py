from typing import Dict, Union

import menus
from blessed import Terminal
from menus.utils import Menu, State


class Interface(Terminal):
    """Main program interface."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.state = State.start

        self.menus: Dict[State, Menu] = {
            State.start: menus.StartMenu(),
            State.highscore: menus.HighScoreMenu(),
            State.file_explorer: menus.ChooseFile(),
            # This gets initialized in the ChooseFile menu
            # State.playing: Game(),
        }

    def render(self) -> None:
        """Clear and render the screen depending on the current state."""
        print(self.clear + self.home + self.menus[self.state].render(self))

    def kinput(self, code: Union[int, None]) -> None:
        """Propogate keyboard input."""
        if code == self.KEY_ENTER:
            self.state = self.menus[self.state].click(self)
            self.selected = 0  # Reset
        else:
            self.selected = self.menus[self.state].kinput(self, code)

    def main(self) -> None:
        """Start the main function taking care of the complete lifetime of the program."""
        while True:
            self.render()
            self.kinput(self.inkey().code)


if __name__ == '__main__':
    term = Interface()
    try:
        with term.fullscreen(), term.cbreak(), term.hidden_cursor():
            term.main()
    except KeyboardInterrupt:
        pass
