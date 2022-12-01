from util import *


@click.group()
def cli():
    pass


def process_line(line):
    return map(int, line.split("\n"))


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    data = [process_line(l) for l in read_file(input, delim="\n\n")]
    sums = [sum(group) for group in data]
    pprint(max(sums))


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    data = [process_line(l) for l in read_file(input, delim="\n\n")]
    sums = [sum(group) for group in data]

    sums.sort()
    pprint(sum(sums[-3:]))


if __name__ == "__main__":
    cli()
