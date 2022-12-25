from util import *


@click.group()
def cli():
    pass


def process_line(line):
    return line


DIR = {
    "<": (-1, 0),
    ">": (1, 0),
    "^": (0, -1),
    "v": (0, 1),
}


def generate_maps(grid):
    base = grid.copy()
    for x, y in base.walk_coords():
        if base.get(x, y) in DIR:
            base.set(x, y, ".")

    w, h = grid.width - 2, grid.height - 2
    blizzards = [(p, grid.get(*p)) for p in grid.walk_coords() if grid.get(*p) in DIR]

    out = [grid]
    while 1:
        next_grid = base.copy()

        next_blizzards = []
        for p, c in blizzards:
            d = DIR[c]
            if c in "<>":
                next_pos = (((p[0] - 1 + d[0]) % w + 1), p[1])
            else:
                next_pos = (p[0], ((p[1] - 1 + d[1]) % h + 1))

            next_blizzards.append((next_pos, c))

        for (x, y), d in next_blizzards:
            next_grid.set(x, y, d)

        if next_grid == out[0]:
            break
        else:
            out.append(next_grid)
            blizzards = next_blizzards
    return out


def shortest_path(start, goal, worlds, start_step=0):
    seen = set()
    q = [(start, start_step)]
    while q:
        curr_pos, steps = q.pop(0)
        world = worlds[steps % len(worlds)]

        seen_pos = (curr_pos, steps % len(worlds))
        if seen_pos in seen:
            continue
        seen.add(seen_pos)

        if world.get(*curr_pos) != ".":
            continue

        if curr_pos == goal:
            return steps

        for next_pos in world.neighbors(*curr_pos):
            if world.get(*next_pos) != "#":
                q.append((next_pos, steps + 1))
        q.append((curr_pos, steps + 1))  # or wait


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    orig_grid = Grid.from_string(input.read())
    worlds = generate_maps(orig_grid)

    start = (1, 0)
    goal = (orig_grid.width - 2, orig_grid.height - 1)
    print(shortest_path(start, goal, worlds))


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    orig_grid = Grid.from_string(input.read())
    worlds = generate_maps(orig_grid)

    start = (1, 0)
    goal = (orig_grid.width - 2, orig_grid.height - 1)

    steps = 0
    for p0, p1 in pairwise([start, goal, start, goal]):
        steps = shortest_path(p0, p1, worlds, start_step=steps)
    print(steps)


if __name__ == "__main__":
    cli()
