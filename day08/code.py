from util import *


@click.group()
def cli():
    pass


def treelines(g, x, y):
    return [
        [(i, y) for i in reversed(range(g.width)) if i < x],
        [(x, j) for j in reversed(range(g.height)) if j < y],
        [(i, y) for i in range(g.width) if i > x],
        [(x, j) for j in range(g.height) if j > y],
    ]


def visible(g, x, y):
    max_height = g.get(x, y)
    for line in treelines(g, x, y):
        if all(g.get(i, j) < max_height for (i, j) in line):
            return True


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    grid = Grid(read_file(input))
    print(sum(1 for (x, y) in grid.walk_coords() if visible(grid, x, y)))


def scenic_score(g, x, y):
    scores = []
    max_height = g.get(x, y)
    for line in treelines(g, x, y):
        visible = first(split_after(line, lambda p: g.get(*p) >= max_height), [])
        scores.append(len(visible))
    return prod(scores)


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    grid = Grid(read_file(input))
    print(max(scenic_score(grid, x, y) for (x, y) in grid.walk_coords()))


if __name__ == "__main__":
    cli()
