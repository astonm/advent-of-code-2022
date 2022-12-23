from util import *


@click.group()
def cli():
    pass


def process_line(line):
    return line


N = (0, -1)
W = (-1, 0)
E = (1, 0)
S = (0, 1)
NW = (-1, -1)
NE = (1, -1)
SW = (-1, 1)
SE = (1, 1)


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    grid = GridN(default=".")
    for y, line in enumerate(read_file(input)):
        for x, c in enumerate(line):
            if c == "#":
                grid.set((x, y), c)

    run_rounds(grid, 10)
    print(sum(1 for (_, c) in grid.walk_all() if c == "."))


def run_rounds(grid, max_rounds=None):
    tries = [
        [(N, NE, NW), N],
        [(S, SE, SW), S],
        [(W, NW, SW), W],
        [(E, NE, SE), E],
    ]

    elves = [p for (p, c) in grid.walk() if c == "#"]

    rounds = range(max_rounds) if max_rounds else count()

    for round in rounds:
        next_pos = {}
        for elf in elves:
            if sum(1 for n in grid.neighbors(elf, diags=True) if n[1] == "#"):
                for dirs, go in tries:
                    if all(
                        grid.get((elf[0] + d[0], elf[1] + d[1])) == "." for d in dirs
                    ):
                        next_pos[elf] = elf[0] + go[0], elf[1] + go[1]
                        break

        if not next_pos:
            break

        duped = {p for (p, n) in Counter(next_pos.values()).most_common() if n > 1}

        next_elves = []
        for elf in elves:
            if elf in next_pos:
                pos = next_pos[elf]
                if pos not in duped:
                    grid.unset(elf)
                    grid.set(pos, "#")
                    next_elves.append(pos)
                    continue
            next_elves.append(elf)

        elves = next_elves
        tries = tries[1:] + [tries[0]]

        check_elves = [p for (p, c) in grid.walk() if c == "#"]
        assert len(elves) == len(check_elves)
        assert sorted(elves) == sorted(check_elves)

    return round + 1


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    grid = GridN(default=".")
    for y, line in enumerate(read_file(input)):
        for x, c in enumerate(line):
            if c == "#":
                grid.set((x, y), c)

    print(run_rounds(grid))


if __name__ == "__main__":
    cli()
