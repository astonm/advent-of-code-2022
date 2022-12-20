from util import *
from llist import *


@click.group()
def cli():
    pass


def process_line(line):
    return int(line)


def shift(l, node, dist):
    target = node.prev
    l.remove_elem(node)

    if dist < 0:
        for i in range(-dist):
            target = target.prev
    else:
        for i in range(dist):
            target = target.next

    l.insert_after(target, node)


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    data = [process_line(l) for l in read_file(input)]
    circle = CircularDoublyLinkedList()

    nodes = []
    for d in data:
        node = circle.append(d)
        nodes.append(node)

    for n in tqdm(nodes):
        shift(circle, n, n.data)

    vals = circle.values()
    z = vals.index(0)
    print(sum(vals[(z + i) % len(vals)] for i in [1000, 2000, 3000]))


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    data = [process_line(l) for l in read_file(input)]
    circle = CircularDoublyLinkedList()

    nodes = []
    for d in data:
        node = circle.append(d * 811589153)
        nodes.append(node)

    for _ in range(10):
        for n in tqdm(nodes):
            shift(circle, n, n.data % (len(data) - 1))

    vals = circle.values()
    z = vals.index(0)
    print(sum(vals[(z + i) % len(vals)] for i in [1000, 2000, 3000]))


if __name__ == "__main__":
    cli()
