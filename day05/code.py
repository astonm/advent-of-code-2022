from util import *


@click.group()
def cli():
    pass


def parse_board(board_string):
    board = board_string.split("\n")
    height = len(board) - 1
    stacks = {}
    for i, c in enumerate(board[height]):
        if c.isnumeric():
            stacks[c] = []
            for y in range(height - 1, -1, -1):
                if i < len(board[y]) and board[y][i].isalpha():
                    stacks[c].append(board[y][i])
    return stacks


def process_line(line):
    return parse("move {:d} from {} to {}", line)


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    board_string, moves = input.read().split("\n\n")
    board = parse_board(board_string)

    for n, src, dest in [process_line(m) for m in moves.strip().split("\n")]:
        for _ in range(n):
            board[dest].append(board[src].pop())
    print("".join(last(s) for s in board.values()))


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    board_string, moves = input.read().split("\n\n")
    board = parse_board(board_string)

    for n, src, dest in [process_line(m) for m in moves.strip().split("\n")]:
        board[dest].extend(board[src][-n:])
        del board[src][-n:]
    print("".join(last(s) for s in board.values()))


if __name__ == "__main__":
    cli()
