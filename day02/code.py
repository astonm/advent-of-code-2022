from util import *


@click.group()
def cli():
    pass


def process_line(line):
    return line.split()


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    def outcome(other, me):
        if other == me:
            return 3
        if me == "A":
            return 0 if other == "B" else 6
        if me == "B":
            return 0 if other == "C" else 6
        if me == "C":
            return 0 if other == "A" else 6

    def score(other, me):
        rename = {"X": "A", "Y": "B", "Z": "C"}
        me = rename[me]
        return "ABC".index(me) + 1 + outcome(other, me)

    data = [process_line(l) for l in read_file(input)]
    scores = [score(*x) for x in data]

    print(sum(scores))


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    def get_me(other, target):
        order = "ABC"
        ind = order.index(other)

        offset = {"X": -1, "Y": 0, "Z": 1}
        return order[(ind + offset[target]) % 3]

    def score(other, target):
        target_scores = {"X": 0, "Y": 3, "Z": 6}
        me = get_me(other, target)
        return "ABC".index(me) + 1 + target_scores[target]

    data = [process_line(l) for l in read_file(input)]
    scores = [score(*x) for x in data]

    print(sum(scores))


if __name__ == "__main__":
    cli()
