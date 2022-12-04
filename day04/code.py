from util import *


@click.group()
def cli():
    pass


def process_line(line):
    def r(s):
        return [int(x) for x in s.split("-")]

    return list(map(r, line.split(",")))


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    data = [process_line(l) for l in read_file(input)]

    def max_span(x, y):
        return [min(x[0], y[0]), max(x[1], y[1])]

    pprint(sum(1 for (l, r) in data if max_span(l, r) in [l, r]))


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    data = [process_line(l) for l in read_file(input)]

    def overlaps(x, y):
        return y[0] <= x[0] <= y[1] or x[0] <= y[0] <= x[1]

    pprint(sum(1 for (l, r) in data if overlaps(l, r)))


if __name__ == "__main__":
    cli()
