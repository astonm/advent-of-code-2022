from util import *


@click.group()
def cli():
    pass


def process_line(line):
    return tuple(map(int, line.split(",")))


dirs = (
    (1, 0, 0),
    (-1, 0, 0),
    (0, 1, 0),
    (0, -1, 0),
    (0, 0, 1),
    (0, 0, -1),
)


def surface_area(pts):
    face_counts = Counter()
    for x, y, z in pts:
        for dx, dy, dz in dirs:
            # each face is described by the two points on either side of it
            p1 = (x, y, z)
            p2 = (x + dx, y + dy, z + dz)

            face = tuple(sorted([p1, p2]))
            face_counts[face] += 1

    # if we see a face more than once, it's interior
    return sum(1 for (f, n) in face_counts.items() if n == 1)


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    data = [process_line(l) for l in read_file(input)]
    print(surface_area(data))


def interior_points(pts):
    pts = set(pts)
    mins = [min(pts, key=lambda d: d[i])[i] for i in range(3)]
    maxs = [max(pts, key=lambda d: d[i])[i] for i in range(3)]

    exterior = set()

    start = tuple(mins)  # decent guess
    assert start not in pts  # make sure it's actually outside

    q = [start]
    seen = {start}
    while q:
        curr = q.pop(0)
        exterior.add(curr)

        for dx, dy, dz in dirs:
            p = curr[0] + dx, curr[1] + dy, curr[2] + dz
            if (
                p not in seen
                and p not in pts
                and mins[0] - 1 <= p[0] <= maxs[0] + 1
                and mins[1] - 1 <= p[1] <= maxs[1] + 1
                and mins[2] - 1 <= p[2] <= maxs[2] + 1
            ):
                seen.add(p)
                q.append(p)

    interior = set()
    for x in range(mins[0], maxs[0] + 1):
        for y in range(mins[1], maxs[1] + 1):
            for z in range(mins[2], maxs[2] + 1):
                p = x, y, z
                if p not in pts and p not in exterior:
                    interior.add(p)
    return interior


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    data = [process_line(l) for l in read_file(input)]
    interiors = interior_points(data)
    print(surface_area(data) - surface_area(interiors))


if __name__ == "__main__":
    cli()
