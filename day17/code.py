from util import *


@click.group()
def cli():
    pass


pieces = [
    x.split("\n")
    for x in """
####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##
""".strip().split(
        "\n\n"
    )
]


def dim(rock):
    return len(rock[0]), len(rock)


def trace(piece, pos):
    for y, line in enumerate(piece):
        for x, c in enumerate(line):
            if c == "#":
                yield (pos[0] + x, pos[1] - y)


def intersects(piece, pos, grid):
    for p in trace(piece, pos):
        if grid.get(p) != ".":
            return True
    return False


def draw(piece, pos, grid, c="#"):
    max_y = 0
    for p in trace(piece, pos):
        grid.set(p, c)
        max_y = max(max_y, p[1])
    return max_y


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    data = read_file(input)[0]

    for n, height in enumerate(run_tetris(data, pieces), start=1):
        if n == 2022:
            return print(height)


def run_tetris(dir_spec, pieces):
    # actually draw the floor!
    grid = GridN(default=".")
    for x in range(1, 8):
        grid.set((x, 0), "-")

    floor = 0
    directions = cycle(dir_spec)
    for ii, piece in enumerate(cycle(pieces)):
        w, h = dim(piece)
        pos = [3, floor + 3 + h]

        # draw the walls, too
        for y in range(floor, floor + 4):
            grid.set((0, y), "|")
            grid.set((8, y), "|")

        while 1:
            dir = next(directions)
            if dir == ">":
                if not intersects(piece, (pos[0] + 1, pos[1]), grid):
                    pos[0] += 1
            if dir == "<":
                if not intersects(piece, (pos[0] - 1, pos[1]), grid):
                    pos[0] -= 1

            if intersects(piece, (pos[0], pos[1] - 1), grid):
                top = draw(piece, pos, grid)
                floor = max(floor, top)
                yield floor
                break
            else:
                pos[1] -= 1


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    data = read_file(input)[0]
    target = 1000000000000

    sample_size = 10_000
    res = run_tetris(data, pieces)
    take(sample_size, res)  # shake off early chaos

    floors = list(take(sample_size, res))
    floor_deltas = deltas(floors)

    cycle_len = None
    cycle_delta = None
    for cycle_guess in range(1, len(floor_deltas)):
        if floor_deltas[:cycle_guess] == floor_deltas[cycle_guess : cycle_guess * 2]:
            cycle_len = cycle_guess
            cycle_delta = floors[cycle_len] - floors[0]
            break

    multiple = (target - sample_size) // cycle_len
    similar_but_smaller = target - multiple * cycle_len
    base_floor = last(take(similar_but_smaller, run_tetris(data, pieces)))
    print(base_floor + multiple * cycle_delta)


if __name__ == "__main__":
    cli()
