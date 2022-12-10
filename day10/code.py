from util import *


@click.group()
def cli():
    pass


def get_register_history(input):
    X = 1
    signal_strengths = []
    inst = input.read().replace("addx", "\n".join(["addx-noop", "add"]))

    for c, line in enumerate(inst.splitlines(), start=1):
        signal_strengths.append((c, X))

        add = parse("add {value:d}", line)
        if add:
            X += add["value"]

    return signal_strengths


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    vals = get_register_history(input)

    def signal_strength(c, X):
        return c * X

    pprint(sum(signal_strength(*vals[i - 1]) for i in range(20, 221, 40)))


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    vals = get_register_history(input)
    picture = Grid([[" "] * 40 for _ in range(6)])

    for c, sprite_pos in vals:
        crt_y, crt_x = divmod(c - 1, 40)  # cycles are 1-indexed, crt pos 0-indexed

        if crt_x in [sprite_pos - 1, sprite_pos, sprite_pos + 1]:
            picture.set(crt_x, crt_y, "#")

    picture.print()


if __name__ == "__main__":
    cli()
