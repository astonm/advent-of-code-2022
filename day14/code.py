from util import *


@click.group()
def cli():
    pass


def process_line(line):
    return [eval(coord) for coord in line.split(" -> ")]


def sign(n):
    if not n:
        return 0
    return -1 if n < 0 else 1


def line(start, end):
    dx, dy = sign(end[0] - start[0]), sign(end[1] - start[1])
    p = list(start)
    end = list(end)

    yield tuple(p)
    while p != end:
        p[0] += dx
        p[1] += dy
        yield tuple(p)


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    grid = GridN(default=".")
    data = [process_line(l) for l in read_file(input)]
    for rock in data:
        for start, end in pairwise(rock):
            for point in line(start, end):
                grid.set(point, "#")

    n_grains = fill_with_sand(grid)
    grid.print()
    print(n_grains)


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    grid = GridN(default=".")
    data = [process_line(l) for l in read_file(input)]
    for rock in data:
        for start, end in pairwise(rock):
            for point in line(start, end):
                grid.set(point, "#")

    n_grains = fill_with_sand(grid, use_infinite_floor=True)
    grid.print()
    print(n_grains)


def fill_with_sand(grid, use_infinite_floor=False):
    lowest_rock = max(grid.bounds()[1])
    infinite_floor = lowest_rock + 2

    sand_source = (500, 0)
    grid.set(sand_source, "+")

    done_filling = False
    for n_grains in count():
        sand_x, sand_y = sand_source

        while 1:
            if grid.get(sand_source) != "+":
                done_filling = True
                break

            if use_infinite_floor:
                if sand_y + 1 == infinite_floor:
                    grid.set((sand_x, sand_y), "o")
                    break
            else:
                if sand_y > lowest_rock:
                    done_filling = True
                    break

            left, down, right = [grid.get((sand_x + i, sand_y + 1)) for i in [-1, 0, 1]]
            if down == ".":
                sand_y += 1
                continue

            if left == ".":
                sand_x -= 1
                sand_y += 1
                continue

            if right == ".":
                sand_x += 1
                sand_y += 1
                continue

            grid.set((sand_x, sand_y), "o")
            break

        if done_filling:
            break

    return n_grains


if __name__ == "__main__":
    cli()
