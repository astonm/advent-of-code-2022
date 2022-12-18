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

    if "ex" in input.name:
        print("didn't solve the example this way")
    else:
        # observation: running the simulation on my input gives a "tetris" full row after placing the 1st piece
        # and that happens starting after piece 1361 and then again every 1715 drops
        # the height of the "tetris" floor increases by 2574 every 1715 drops
        target = 1000000000000
        assert target >= 1361  # below 1361, pattern doesn't hold
        repeats, remainder = divmod(target - 1361, 1715)

        pattern_repeated_floor = repeats * 2574
        addon = last(take(remainder + 1361, run_tetris(data, pieces)), 0)

        print(pattern_repeated_floor + addon)


if __name__ == "__main__":
    cli()
