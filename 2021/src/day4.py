import os
import re
import logging
import argparse
from utils import readline_input_file, readlines_input_file, matrix_to_str, initialize_logging

INPUT_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'inputs/bingo_input')


class Board:
    def __init__(self, boards_data):
        self.board_grid = self.load_board(boards_data)
        self.marked_grid = self.create_marked_grid()
        self.has_won = False

    def load_board(self, board_data):
        board = []

        for row in board_data:
            board.append([int(draw) for draw in re.findall(r'\d+', row.replace('\n', ''))])

        return board

    def create_marked_grid(self):
        marked = []

        for row in range(len(self.board_grid)):
            marked.append([False]*5)

        return marked

    def mark_board(self, row, col):
        logging.debug(f"Marked row:{row}, col:{col}")
        self.marked_grid[row][col] = True

    def get_board_score(self, just_called):
        unmarked = 0

        for i in range(len(self.marked_grid)):
            for j in range(len(self.marked_grid[0])):
                unmarked = unmarked+self.board_grid[i][j] if self.marked_grid[i][j] is False else unmarked

        return unmarked*just_called

    def find_number(self, number):
        for i in range(len(self.board_grid)):
            for j in range(len(self.board_grid[i])):
                if number == self.board_grid[i][j]:
                    logging.debug(f"Found {number} in row:{i}, col:{j}")
                    return i, j

        return None, None

    def won(self):
        column_marked = [0]*len(self.marked_grid[0])

        for i in range(len(self.marked_grid)):
            if self.marked_grid[i] == [True]*5:
                logging.debug(f"The following row has won: {self.board_grid[i]} / {self.marked_grid[i]}")
                self.has_won = True
                return True

            for j in range(len(self.marked_grid[i])):
                column_marked[j] = column_marked[j]+1 if self.marked_grid[i][j] is True else column_marked[j]
                if column_marked[j] == len(self.marked_grid):
                    logging.debug(f"The following board has reached {column_marked[j]} marks:"
                                  f"{matrix_to_str(self.board_grid)}\n{matrix_to_str(self.marked_grid)}")
                    self.has_won = True
                    return True

        return False

    def __repr__(self):
        return '[' + ', '.join(map(str, self.board_grid)) + ']'


class Bingo:
    def __init__(self, file_path):
        self.draws = self.load_draws(file_path)
        self.boards = self.load_boards(file_path)

    def load_draws(self, file_path):
        draws = readline_input_file(file_path)

        return [int(draw) for draw in draws.replace('\n', '').split(',')]

    def load_boards(self, file_path):
        boards_data = readlines_input_file(file_path)[2:]
        board_data = []
        boards = []
        board_row = 0

        while len(boards_data) > 0:
            if len(boards_data) > 5:
                while boards_data[board_row] != '\n':
                    board_data.append(boards_data[board_row])
                    board_row += 1
            else:
                for i in range(5):
                    board_data.append(boards_data[board_row])
                    board_row += 1

            boards.append(Board(board_data))
            # reset
            board_data.clear()
            boards_data = boards_data[6:]
            board_row = 0

        return boards

    def won(self, board):
        return self.boards[board].won()

    def draw_number(self):
        drawn = self.draws.pop(0)
        logging.debug(f"Number drawn: {drawn}")
        return drawn

    def mark_number(self, board, number):
        row, col = self.boards[board].find_number(number)

        if row is not None and col is not None:
            self.boards[board].mark_board(row, col)

    def play(self, goal='win'):
        boards_left = 1 if goal == 'win' or goal is None else len(self.boards)
        draws_left = len(self.draws)
        last_board = None
        last_draw = None

        while boards_left and draws_left:
            number_drawn = self.draw_number()
            draws_left -= 1

            for i in range(len(self.boards)):
                if not self.boards[i].has_won and boards_left:
                    logging.debug(f"Going to mark {number_drawn} in {i} board.")
                    self.mark_number(i, number_drawn)
                    logging.debug(f"Board {i} marks: {matrix_to_str(self.boards[i].marked_grid)}")
                    if self.won(i):
                        logging.debug(f"Board {i} has won")
                        boards_left -= 1
                        logging.debug(f"Boards left: {boards_left}")
                        if boards_left == 0:
                            last_board = i
                            last_draw = number_drawn
                            break

        if last_board is not None and last_draw is not None:
            winner_score = self.boards[i].get_board_score(number_drawn)
            logging.info(f"Winner board score: {winner_score}")

            return winner_score


def get_parameters():
    parser = argparse.ArgumentParser(add_help=False)

    parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS,
                        help='Show this help message and exit.')
    parser.add_argument('-d', '--debug', action='count', dest='debug_level',
                        help="Enable debug messages.")
    parser.add_argument('--goal', dest='goal', choices=['win', 'lose'],
                        help="Specifies the strategy to follow. If you want to let the squid win, use lose. "
                             "But if you want to win, use win.")

    return parser.parse_args()


def set_parameters(args):
    if args.debug_level:
        initialize_logging('DEBUG')
    else:
        initialize_logging('INFO')


def main():
    args = get_parameters()
    set_parameters(args)
    new_bingo = Bingo(INPUT_PATH)

    new_bingo.play(args.goal if args.goal else None)


if __name__ == '__main__':
    main()
