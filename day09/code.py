from util import *


@click.group()
def cli():
    pass


def process_line(line):
    return parse("{} {:d}", line)


deltas = {
    "U": Vector([0, 1]),
    "D": Vector([0, -1]),
    "L": Vector([-1, 0]),
    "R": Vector([1, 0]),
}


def sign(n):
    if not n:
        return 0
    return -1 if n < 0 else 1


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    head_pos = Vector([0, 0])
    tail_pos = Vector([0, 0])
    tail_seen = {tuple(tail_pos)}

    data = [process_line(l) for l in read_file(input)]
    for dir, dist in data:
        for _ in range(dist):
            head_pos += deltas[dir]

            dx, dy = head_pos - tail_pos
            if dx * dx + dy * dy > 2:
                tail_pos += Vector([sign(dx), sign(dy)])

            tail_seen.add(tuple(tail_pos))

    print(len(tail_seen))


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    snake = [Vector([0, 0]) for _ in range(10)]
    tail_seen = {tuple(snake[-1])}

    data = [process_line(l) for l in read_file(input)]
    for dir, dist in data:
        for _ in range(dist):
            snake[0] += deltas[dir]

            for head, tail in pairwise(snake):
                dx, dy = head - tail
                if dx * dx + dy * dy > 2:
                    tail += Vector([sign(dx), sign(dy)])

            tail_seen.add(tuple(snake[-1]))

    print(len(tail_seen))


if __name__ == "__main__":
    cli()
