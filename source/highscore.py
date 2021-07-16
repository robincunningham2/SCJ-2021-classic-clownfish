import os
from operator import itemgetter

from table import make_table


class Highscore:
    """Highscore Class"""

    filename = os.path.dirname(__file__) + '/../resources/highscore.csv'
    highscore = []  # List of Dictionary entries with following keys: 'Puzzle', 'Name', 'Time', 'Moves'

    def __init__(self):
        self.__read()

    def add(self, image: str, player_name: str, time: int, moves: int) -> None:
        """Adds new highscore to the list

        :param image: Name of the image for which to store the highscore
        :param player_name: Name of the player for whom to add a highscore
        :param time: Time (in seconds) used by the player so solve the puzzle
        :param moves: Moves needed by the player to solve the puzzle
        """
        self.highscore.append({'Puzzle': image, 'Name': player_name, 'Time': time, 'Moves': moves})
        self.__save_entry()

    def display(self, puzzle: str, sort: str = 'Time') -> str:
        """Display the player highscore

        :param puzzle: Name of the puzzle for which to show the highscore
        :param sort: Sort the highscore after Time or Moves. Default is Time.
        :return: Returns the highscore as a table
        """
        # get highscores for requested puzzle
        highscore = []
        for entry in self.highscore:
            if entry['Puzzle'] == puzzle:
                highscore.append(entry)
        if len(highscore) == 0:
            return 'No highscore for this puzzle available.'

        # sort the highscore
        if sort == 'Time':
            highscore = sorted(highscore, key=itemgetter('Time'))
        elif sort == 'Moves':
            highscore = sorted(highscore, key=itemgetter('Moves'))

        table = make_table(
            rows=[[entry['Puzzle'], entry['Name'], entry['Time'], entry['Moves']] for entry in highscore],
            labels=['Puzzle', 'Name', 'Time', 'Moves'])

        return table

    def delete(self) -> None:
        """Deletes all highscores"""
        self.highscore.clear()
        os.remove(self.filename)  # file will be created again when saving new data

    def __save_entry(self) -> None:
        try:
            with open(self.filename, mode='a') as file:
                values = list(dict(self.highscore[-1]).values())
                values = [str(value) for value in values]
                file.write(','.join(values))
        except FileNotFoundError:
            pass  # TODO: error handling

    def __read(self) -> None:
        try:
            with open(self.filename) as file:
                lines = file.readlines()
                for line in lines:
                    entry = line.strip().split(',')
                    self.highscore.append({'Puzzle': entry[0], 'Name': entry[1],
                                           'Time': int(entry[2]), 'Moves': int(entry[3])})

        except FileNotFoundError:
            pass  # TODO: error handling
