from util import *


@click.group()
def cli():
    pass


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    for line in read_file(input):
        for i, window in enumerate(windowed(line, 4)):
            if len(set(window)) == 4:
                print(i + 4)
                break


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    for line in read_file(input):
        for i, window in enumerate(windowed(line, 14)):
            if len(set(window)) == 14:
                print(i + 14)
                break


if __name__ == "__main__":
    cli()
