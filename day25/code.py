from util import *


@click.group()
def cli():
    pass


vals = {
    "2": 2,
    "1": 1,
    "0": 0,
    "-": -1,
    "=": -2,
}
rvals = {v: k for (k, v) in vals.items()}


def process_line(line):
    return [vals[c] for c in line]


def snafu_to_decimal(l):
    return sum(x * 5 ** y for (x, y) in zip(l, reversed(range(len(l)))))


def decimal_to_snafu(n):
    out = []
    while n:
        n, r = divmod(n, 5)
        if r > 2:
            r = r - 5
        if r < 0:
            n += 1
        out.append(rvals[r])

    return "".join(reversed(out))


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    data = [process_line(l) for l in read_file(input)]
    print(decimal_to_snafu(sum(snafu_to_decimal(s) for s in data)))


if __name__ == "__main__":
    cli()
