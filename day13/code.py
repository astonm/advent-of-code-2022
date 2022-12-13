from util import *


@click.group()
def cli():
    pass


def process_line(line):
    return tuple(map(json.loads, line.split("\n")))


def cmp(val1, val2):
    if isinstance(val1, int) and isinstance(val2, int):
        # https://docs.python.org/3.0/whatsnew/3.0.html#ordering-comparisons
        return (val1 > val2) - (val1 < val2)

    if isinstance(val1, int):
        return cmp([val1], val2)

    if isinstance(val2, int):
        return cmp(val1, [val2])

    for l, r in zip(val1, val2):
        if cmp(l, r) == -1:
            return -1
        if cmp(l, r) == 1:
            return 1

    return (len(val1) > len(val2)) - (len(val1) < len(val2))


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    data = [process_line(l) for l in read_file(input, "\n\n")]
    print(sum(i for i, pair in enumerate(data, start=1) if cmp(*pair) == -1))


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    data = [json.loads(l) for l in read_file(input)]
    data.append([[2]])
    data.append([[6]])

    data.sort(key=cmp_to_key(cmp))
    print(prod(data.index(v) + 1 for v in ([[2]], [[6]])))


if __name__ == "__main__":
    cli()
