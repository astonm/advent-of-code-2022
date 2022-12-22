from util import *


@click.group()
def cli():
    pass


class Face(IntEnum):
    Right = 0
    Down = 1
    Left = 2
    Up = 3


DIRS = {
    Face.Right: (1, 0),
    Face.Down: (0, 1),
    Face.Left: (-1, 0),
    Face.Up: (0, -1),
}

ICON = {
    Face.Right: ">",
    Face.Down: "v",
    Face.Left: "<",
    Face.Up: "^",
}


def wraparound_flat(grid, facing, pos):
    before = pos
    if facing == Face.Right:
        pts = zip(range(grid.width), repeat(pos[1]))
    if facing == Face.Left:
        pts = zip(reversed(range(grid.width)), repeat(pos[1]))
    if facing == Face.Down:
        pts = zip(repeat(pos[0]), range(grid.height))
    if facing == Face.Up:
        pts = zip(repeat(pos[0]), reversed(range(grid.height)))

    for x, y in pts:
        if grid.get(x, y, " ") != " ":
            return (x, y), facing


def walk_map(input, wraparound):
    pic, path = input.read().split("\n\n")
    grid = Grid.from_string(pic)

    instructions = re.split(r"(R|L)", path.strip())

    pos = first(c for c in grid.walk_coords() if grid.get(*c) == ".")
    facing = Face.Right

    grid.set(pos[0], pos[1], ICON[facing])

    for inst in instructions:
        if inst.isnumeric():
            for _ in range(int(inst)):
                dx, dy = DIRS[facing]
                next_pos = (pos[0] + dx, pos[1] + dy)
                next_facing = facing
                c = grid.get(*next_pos, " ")

                if c == " ":
                    next_pos, next_facing = wraparound(grid, facing, next_pos)
                    c = grid.get(*next_pos, " ")

                if c == "#":
                    break

                pos = next_pos
                facing = next_facing
                grid.set(pos[0], pos[1], ICON[facing])
        else:
            df = 1 if inst == "R" else -1
            facing = Face((facing + df) % 4)
            grid.set(pos[0], pos[1], ICON[facing])

    return pos, facing


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    pos, facing = walk_map(input, wraparound=wraparound_flat)
    print(1000 * (pos[1] + 1) + 4 * (pos[0] + 1) + facing)


@cli.command()
@click.argument("input", type=click.File())
def print_corners(input):
    # just parse the map and print where the obvious corners are
    pic, _ = input.read().split("\n\n")
    grid = Grid.from_string(pic)

    ly = -1
    for x, y in grid.walk_coords():
        n = sum(1 for (nx, ny) in grid.neighbors(x, y) if grid.get(nx, ny) != " ")
        if n == 2:
            print((x, y))
            if ly != y:
                print()
            ly = y


def edge_maker(size):
    def edge(p1, d1, p2, d2, forward_dir, reverse_dir):
        assert all(x % size in [0, size - 1] for x in p1), p1
        assert sum(abs(x) for x in d1) == 1, d1
        assert all(x % size in [0, size - 1] for x in p2), p2
        assert sum(abs(x) for x in d2) == 1, d2

        out = {}
        for i in range(size):
            a = p1[0] + d1[0] * i, p1[1] + d1[1] * i
            b = p2[0] + d2[0] * i, p2[1] + d2[1] * i
            out[a] = (b, forward_dir)
            out[b] = (a, reverse_dir)

        return out

    return edge


def get_wraparound(edges, facing, pos):
    dx, dy = DIRS[facing]
    prev_pos = pos[0] - dx, pos[1] - dy
    assert prev_pos in edges, (pos, prev_pos)
    return edges[prev_pos]


def wraparound_cube_ex(_, facing, pos):
    edge = edge_maker(size=4)
    edges = (
        {}
        | edge((8, 0), (1, 0), (8, 11), (1, 0), Face.Up, Face.Down)  # 1/5
        | edge((11, 0), (0, 1), (15, 11), (0, -1), Face.Left, Face.Left)  # 1/6
        | edge((8, 0), (0, 1), (4, 4), (1, 0), Face.Down, Face.Right)  # 1/3
        | edge((11, 4), (0, 1), (15, 8), (-1, 0), Face.Down, Face.Left)  # 4/6
        | edge((0, 4), (0, 1), (15, 11), (-1, 0), Face.Up, Face.Right)  # 2/6
        | edge((0, 4), (1, 0), (11, 0), (-1, 0), Face.Down, Face.Down)  # 2/1
        | edge((0, 7), (1, 0), (11, 11), (-1, 0), Face.Up, Face.Up)  # 2/5
    )
    return get_wraparound(edges, facing, pos)


def wraparound_cube(grid, facing, pos):
    edge = edge_maker(size=50)
    edges = (
        {}
        | edge((50, 0), (1, 0), (0, 150), (0, 1), Face.Right, Face.Down)  # 1/6 U->L
        | edge((50, 0), (0, 1), (0, 149), (0, -1), Face.Right, Face.Right)  # 1/4 L->L
        | edge((100, 49), (1, 0), (99, 50), (0, 1), Face.Left, Face.Up)  # 2/3 D->R
        | edge((149, 0), (0, 1), (99, 149), (0, -1), Face.Left, Face.Left)  # 2/5 R->R
        | edge((100, 0), (1, 0), (0, 199), (1, 0), Face.Up, Face.Down)  # 2/6 U->D
        | edge((50, 50), (0, 1), (0, 100), (1, 0), Face.Down, Face.Right)  # 3/4 L->U
        | edge((50, 149), (1, 0), (49, 150), (0, 1), Face.Left, Face.Up)  # 5/6 D->R
    )
    return get_wraparound(edges, facing, pos)


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    wraparound = wraparound_cube_ex if "ex" in input.name else wraparound_cube
    pos, facing = walk_map(input, wraparound)
    print(1000 * (pos[1] + 1) + 4 * (pos[0] + 1) + facing)


if __name__ == "__main__":
    cli()
