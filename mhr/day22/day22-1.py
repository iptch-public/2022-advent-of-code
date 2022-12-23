import re
from dataclasses import dataclass

from common import load_lines, print_grid


@dataclass
class Move:  # first move, then turn
    steps: int
    turn: str  # turn direction L or R or S (straight)


def parse_path(path: str) -> list[Move]:
    amounts_strings = re.findall('[0-9]+', path)
    moves = []
    pointer = len(amounts_strings[0])  # points to idx of turn letter
    for move_idx, steps_str in enumerate(amounts_strings):
        current_turn = path[pointer:pointer + 1]

        if move_idx == len(amounts_strings) - 1:
            moves.append(Move(int(steps_str), 'S'))
            continue

        moves.append(Move(int(steps_str), current_turn))
        pointer += 1 + len(amounts_strings[move_idx + 1])
    return moves


def to_str(list_of_strings: list[str]) -> str:
    return ''.join(list_of_strings)


def get_start_position_indices(grid: list[list[str]]) -> tuple[int, int]:
    return 0, idx_first_non_whitespace(to_str(grid[0]))


def get_new_facing(current: str, turn: str) -> str:
    if turn == 'S':
        return current
    transition_map = {
        ('R', 'L'): 'U',
        ('R', 'R'): 'D',
        ('D', 'L'): 'R',
        ('D', 'R'): 'L',
        ('L', 'L'): 'D',
        ('L', 'R'): 'U',
        ('U', 'L'): 'L',
        ('U', 'R'): 'R',
    }
    return transition_map[(current, turn)]


def compute_password(grid: list[list[str]], moves: list[Move]) -> int:
    row_idx, col_idx = get_start_position_indices(grid)
    facing_symbol = {'R': '>', 'D': 'v', 'L': '<', 'U': '^'}
    facing = 'R'
    for move_idx, move in enumerate(moves):
        for _ in range(move.steps):
            try:
                grid[row_idx][col_idx] = facing_symbol[facing]
                # print(f'({row_idx}, {col_idx}):  {facing}')
                row_idx, col_idx = calculate_next(grid, (row_idx, col_idx), facing)
            except NextPositionOccupied:
                break  # stay where we are
        facing = get_new_facing(facing, move.turn)

    facing_value = {'R': 0, 'D': 1, 'L': 2, 'U': 3}
    password = 1000 * (row_idx + 1) + 4 * (col_idx + 1) + facing_value[facing]

    print(f'Final position: ({row_idx + 1}, {col_idx + 1}) {facing}')
    print(f'Did {move_idx + 1} / {len(moves)} moves')
    return password


def idx_first_non_whitespace(line: str) -> int:
    return len(line) - len(line.lstrip())


class NextPositionOccupied(Exception):
    pass


def calculate_next(grid: list[list[str]], position: tuple[int, int], facing: str) -> tuple[int, int]:
    height, width = len(grid), len(grid[0])
    row_idx, col_idx = position

    if facing == 'R':
        if (col_idx == width - 1) or (grid[row_idx][col_idx + 1] == ' '):
            col_idx = idx_first_non_whitespace(to_str(grid[row_idx]))
        else:
            col_idx += 1
    elif facing == 'D':
        if (row_idx == height - 1) or (grid[row_idx + 1][col_idx] == ' '):
            row_idx = idx_first_non_whitespace(to_str([line[col_idx] for line in grid]))
        else:
            row_idx += 1
    elif facing == 'L':
        if (col_idx == 0) or (grid[row_idx][col_idx - 1] == ' '):
            col_idx = len(grid[row_idx]) - 1 - idx_first_non_whitespace(to_str(grid[row_idx][::-1]))
        else:
            col_idx -= 1
    elif facing == 'U':
        if (row_idx == 0) or (grid[row_idx - 1][col_idx] == ' '):
            row_idx = len([line[col_idx] for line in grid][::-1]) - 1 - idx_first_non_whitespace(
                to_str([line[col_idx] for line in grid][::-1]))
        else:
            row_idx -= 1
    else:
        raise RuntimeError('unexpected facing')

    if grid[row_idx][col_idx] == '#':
        raise NextPositionOccupied()

    return row_idx, col_idx


if __name__ == '__main__':
    PATH = '35L7L12L18R42R25R24R32R34L11L17L42L47L6L39L4R46R23L24L20L7R14R9R27R34R30L48R30L11L37R50R47L42L9L14R42R50R33L4R33L22R5L39R40R14L23L10R36L15L25R6R13L44L43L39L1R21L1L23R18R13R9R22R8R2L50L44L16R1R19L35L10R29L23L39L30R2R14L3L8L28R35R3R9R27R19R44L5L31L16R24R4L41R32R12R1L48R10R24R17R38L25R20L14L37L43L7L18L13R9L30L47L30L37R18R6R7R20R17R9R5R9R17L30L21R35L21L2L34L16L42R30R29R37L16R39R35L20L43R37R25R8L38L43L22L36R41R13R16L5L20R9R7R25L9L46L6L12L10R8R27R39R16R6R10L10R38L37L29L3R46R12L25R21R32R20R47R16L9R22L23L1R34L48R39L33R39R36L11R13R28R17L48L22R12L47L48L19R15L48L14R2L11L43R42R15L19R19L43R22R40L39L48L10R31L47L26R6R37R4R6R1L13R8L32R9L32R40R12L19L18R41L14R28L45L49L1R27R4L37L11L47L17R32L44R20R3R8R3L17L43R21L24L19L44L49L50R40R7R9R12R15R45L14L31L39L39R18L36L41L11R38L39L31R48R37L37L33R50R21R27L37R34R36L29R23L17R8L43R12R10R33R40L43R15R16R4L1L8L32R13L20L3L24L42L28L27R31R28L9R42L36L41L5R24R4L1R24R24L23R15R41L26L20R37L22L37R20R36R9R38L39L22L10L24L9R17L30R13L15R14R17R29L49L3R10R16R19L28L42L50R49L46R5R37R49L11R12R25R18L30L27L4R3R26L1R3R21R6L7R21L7R12R47R27L48R35L27R21R13R13R30R31R2L10L28R18L19L24L31R42R23L37R33L39L2R25L2R12R5R23R7R28L3R3R42R5L25R22R27L42R18L45R50R22L22L8L48R49L15R41R43R41L36L20L30R24R2R29R25R49L44L46R21L34L46R38L39R42R45R34R38R15R39L31R16R36L2L19R29R33R35L39R6R32L20R27L20L40L35R2R41R24R37R17R9L41L14L50L16L46L33L6L31R16R45R40R5R29R25R4L47R33L31R27L25L1L50R26L38L28L38L8L36R10L47L8R36R49R7L35R13L30L23L30R6L33L8R9L21R19L11R27L35R20L8L36R31L50R7L10R2R13L15R26R38R7R8L49L28R1R13L45R7L6L14R11R1R40L27L16L26L49R34R42R38R30L41L14R8L42L50R1L22R45L48R26L5R24R41L15R33R5R25L40R4R43R44L35L5R50R40R8L36L23R47L36L38R36L50L37L45R15L45L31L24L49R31R7L25R9R37R33R46R10R27L3L40R28R25R48L39L12R19L49L24R49L16L42L31R34R42L31L43R2R50R24L35R32R12R48R24L7R2R44R2R45R36L24R46L50R43L4L49L38L15R22L42L2L26R3L24R40R9R8L33L20R26L48R33R15L48L20R47R25R14L31L21R26R12L37L29L41R10L15R9R30R19L7L46L36R39R12L44R46R48R12R19R18R48L27R4R17L21R15R41R2L41R7R27L18L30L26L10R31R46L19R36L23L37R4R48L25L23R6L6L48L34L32R14L36R37R12R19R4R20L32R3L6L21L21R23R14R13R39R24L15R7R17L24L43L27L35L14R3R38L24L47L24R10L23R6L31R45R22R16L6L33R27R49L29L12R21R28R30R25R21L41L33L35R8L33R28R47L45R35R27R39R28R18R35R39R40L29R12R19R40L50R37R4R28R30L5R41R30L29R50R33L1L41L12R16L49R41R4R17L27R10R40L34R40L47R34L21L40L42L37L5R28R6R34L47L11R27L37R31R40L46R49L25R50R2L20L7R24R16L33R40R50L37R11R14L31R3L37R16L36R32L28L37R47L17L11L28L37L46R31L27L8R7R17R44R46R8L35L13L21R43L17R44L4L20L27R39L38R32L6L37L26R20R38L22L48R2L14R8L5L30R6R40L27L38R1R35R50L9L25R43L25L13R21L25L10L38R50R40L31R50R48L49L22R30L45R44R17L15R5L49R12L36L1R10R2L10L11L2R3R2R35L14L29L32R46R13R38L23R39L29L44L2R27L38R5L30R43R32L42L6R41L28L32R23L2L17R37R9R28R28L24R20L1L22R46R36L32L42R37R6R34L26L27R34L29R32L28L19R8R38L33L41L30R22R2R46L37L19R39R9R41R10R32L37L7R35R41R19L8L40L33R24L49R50L49R19R3R44L42R46L19R28L9R40L41L45L25R25L22R42L34L9R32R4R22R27L24R31L26R27R15R25L34R35L30L13R26L8R3R26L33R25L46R35R50L25R31R10R31R16L26L41R45L37R32R34L5R2R45L14R15L10R32L19R49L50L27L39R46R34R2R28L17L19L47L25R8R30L27R41L5L48L50L14L29L13R35L10L16R43R43L33L39R42L27R17L22R30R25R36R21R37L9L30L49R41L27R26R28L25L36R3R23L25L13L38L29R26L26R15R27L6L40R18R31L47R7L31L26R36R42L34R46R37R10R28L1L9R17L22L39R50L47R1L7R33L7R11L44R20R23R49L27R40L33L28R15R43R39R32L20L1L34L38R17L41L6L39R41L20L4L48R1R14L12R28L33R23R8R8L3R47L30R36R16L10L38R9L15R46L32R14L17L13L17L38R16L39L31R14R36R32R34R17L18R6R34L36L9R40L4L5R2L33R2R46R3R41L45L20L20L36R30L20R19L1L48L38R6R33L19R15L7L12R21L41L10L17R13R14R15R27R35R2R12L48R23L30L29R19R34R11R17R37L21L24R8R49R23L37L44R13R39R3L8R43L20R23L2R28R12R35L3R38L43L28L42R3L48R13L42L8L7R29L32R9R49L33R8R10L35R39L46R7L45L44L5L49L14R15L24L4L32L7L9L8R36L36R12R44L5L4L40L23R28R20R36R3L3R48L50R38L40L9R25R34L31R19L26L27R12R28R19R8L47L40R29L45R16R34R1L18L11L13R22L28R29R6R15R25R7L37L4R32R46R49R36R28L5L4R24R43R10L16R21R25L5R32R10R26R18R6R42R4L48R41L11L31L27R20L48R18L25L21L30L39L1L40R33L18R25R9L47R41R15R13R41R42R43R4R45R13R11L15R41R42R11L21R26R7R3R48L50L4L33L26R25L27L10R38L42L22L43R29L21L16L32L38R13L2R9R10L45L25L11R2L4R43R50R25L26L17R44R47L30R38R49R38R3R13L47L39R46L8R15R9R3L47R7L12L11L13L2R6L7R24R9L11R25R50L45R41R17R6R1R9L8L21R26R36L18R5R43L6R28L12R26R21R36L44L47R37L21R18R18R22L6R19R12R20R40L11R32R49R13R1L1L3R43R37R10L19L15L13R29L3L29L18L21R5L27R7L34L32R24L36L18R15L45R22R41L32L42R23R39R22R19L31R31R17L28R38L6R11R34L13L44L49L24L10R2L18R27L47R21L45L3L4L49L18L18L29L45R32R6L28R44L30L20L47R29L21L49R50R13L21L31R28L6L27L1L20L40R50R32R19R19R11L48R43L33L8R38R4L33R11L33L33R42R15L39L21R39L37R45L44L13R15L9R23L47L17R11R5R45L2L43R22R18R36L33R29L18R38L22R28L6L43L49R29L16L22R47L43R24R26R45R10R35R6L12L12L3L23R23R29L50L25R35L6R6L35R3R27R38L28L43L13R14L29L21L35R36L45R47R39L5L34L11R49L14R48L34R23R26R33L45R4L10R19L50L42R5L37L22R41L40R21L47R25R16R8L36R46R7L35L14R48R43L2L39L34R29R1L38R33L4L29R13R50L8L4L35L7R18L1R37R24L22L1R22R22L11R21L37L2L35L21R49R10R2L39L30R17L47R6R38L6L43L8R30L16L33L40L9R33L47R44R49L2R31L21R41R4L25L47L28L6R8R43R46R24R9L6R21L18R24L16L41L6R12L27R31R10L6R21L36R13R6L33R4L8R27L49R13R25L9R44L41L19R35L49L18R9R41R13R27R9L30L50L10R8R2R48R50L47R34R25L5L23L16R37L37L31L8L21L45L18L10L9R9R9L46L2L43L32R11R30L46L23R26R3R26L35L46R6R4R2R17R30R31R9L48R45L38R27L48L9R15L29R43R42L8L17R14R49L16L1R26R9R28R20L10R18R28R47L50R27L41R34R18L39L16L28L38R42L26L41L44R49L17L22L30R34L9L30L29R11R13R16R5R18R6R14L21L26R50R49R41R25R47R18R2R21L20R11R6R3R33L44L34L38R7L37R6R6R44L18L40L18R24R32R6L38R38L18R10R39R34L12R25L45R20L38L27R13L48R37R45R45L6R29R15L36R16R16R27R19L33L44R7R29L42R42L20R26L12R47L23L19R47L47R5R30R48R46L8R33L44L8R22R42R17R24L39L35L28L41L50L42R23L18L17R43R17L14R25L32L14L36L39R46L12R4L15R44L11L32R38R11L6L7L30L7R37L14R6L37L20R32L23L32L39'
    TEST_PATH = '10R5L5R10L4R5L5'
    TEST = False

    lines_ = load_lines(day=22, file_name='input.txt' if not TEST else 'test_input.txt',
                        skip_empty_lines=True, do_strip=False)
    moves_ = parse_path(PATH if not TEST else TEST_PATH)
    grid_ = [list(line[:-1]) if idx < len(lines_) - 1 else list(line) for idx, line in enumerate(lines_)]
    for line in grid_:
        assert len(line) == len(grid_[0])

    password_ = compute_password(grid_, moves_)
    print_grid(grid_)

    print(f'Task 1: {password_} is the password')
