import os
import re
from utils import readlines_input_file

INPUT_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'inputs/vents_lines')


def get_vents_lines(data):
    vents_lines = []

    for i in range(len(data)):
        line = re.findall(r'\d+', data[i])

        for i in range(len(line)):
            line[i] = int(line[i])

        vents_lines.append(line)

    return vents_lines


def get_rows_and_cols(lines):
    max_x, max_y = 0, 0

    for x1, y1, x2, y2 in lines:
        if x1 > x2 and x1 > max_x:
            max_x = x1
        elif x2 > max_x:
            max_x = x2

        if y1 > y2 and y1 > max_y:
            max_y = y1
        elif y2 > max_y:
            max_y = y2

    return max_x+1, max_y+1


def create_diagram(lines):
    diagram = []
    rows, cols = get_rows_and_cols(lines)

    for i in range(rows):
        diagram.append([0]*cols)

    return diagram


def update_diagram(diagram, vents_lines):
    for x1, y1, x2, y2 in vents_lines:

        # horizontal line
        if x1 == x2:
            for i in range(abs(y1-y2)+1):
                diagram[x1][y1-i if y1 > y2 else y2-i] += 1

        # # vertical line
        elif y1 == y2:
            for i in range(abs(x1-x2)+1):
                diagram[x1-i if x1 > x2 else x2-i][y1] += 1

        # diagonal line
        if x1-y1 == x2-y2 or x1+y1 == x2+y2:
            for i in range(abs(y1-y2)+1):
                diagram[x1-i if x1 > x2 else x1+i][y1-i if y1 > y2 else y1+i] += 1


def lines_overlapping_count(lines_number, diagram):
    n_rows, n_cols = len(diagram), len(diagram[0])
    count = 0

    for i in range(n_rows):
        for j in range(n_cols):
            if diagram[i][j] >= lines_number:
                count += 1

    return count


def main():
    vents_lines = get_vents_lines(readlines_input_file(INPUT_PATH))
    diagram = create_diagram(vents_lines)
    n_lines_overlap = 2

    update_diagram(diagram, vents_lines)
    print(f"Times that at least {n_lines_overlap} overlap: {lines_overlapping_count(n_lines_overlap, diagram)}")


if __name__ == "__main__":
    main()
