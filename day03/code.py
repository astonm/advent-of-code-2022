from util import *


@click.group()
def cli():
    pass


prio = "_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def intersect(char_sets):
    out = set(char_sets[0])
    for char_set in char_sets[1:]:
        out &= set(char_set)
    return first(out)


def process_line(line):
    l = len(line)
    a, b = line[: l // 2], line[l // 2 :]
    return intersect([a, b])


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    data = [process_line(l) for l in read_file(input)]
    pprint(sum(prio.index(d) for d in data))


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    lines = read_file(input)
    data = [intersect(group) for group in grouper(lines, 3)]
    pprint(sum(prio.index(d) for d in data))


if __name__ == "__main__":
    cli()
