from util import *


@click.group()
def cli():
    pass


def process_line(line):
    return list(line)


def find_min_steps(grid, start, end):
    q = [(start,)]
    seen = set()
    while q:
        path = q.pop(0)
        pos = path[-1]

        if pos in seen:
            continue
        seen.add(pos)

        if pos == end:
            return len(path) - 1

        for next_pos in grid.neighbors(*pos):
            if ord(grid.get(*next_pos)) <= ord(grid.get(*pos)) + 1:
                q.append(path + (next_pos,))

    return inf


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    grid = Grid([process_line(l) for l in read_file(input)])
    start = first(c for c in grid.walk_coords() if grid.get(*c) == "S")
    end = first(c for c in grid.walk_coords() if grid.get(*c) == "E")

    grid.set(start[0], start[1], "a")
    grid.set(end[0], end[1], "z")

    print(find_min_steps(grid))


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    grid = Grid([process_line(l) for l in read_file(input)])
    start = first(c for c in grid.walk_coords() if grid.get(*c) == "S")
    end = first(c for c in grid.walk_coords() if grid.get(*c) == "E")

    grid.set(start[0], start[1], "a")
    grid.set(end[0], end[1], "z")

    starts = [c for c in grid.walk_coords() if grid.get(*c) == "a"]
    print(min(find_min_steps(grid, start, end) for start in starts))


if __name__ == "__main__":
    cli()
