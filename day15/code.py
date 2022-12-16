from util import *


@click.group()
def cli():
    pass


def process_line(line):
    res = parse("Sensor at x={:d}, y={:d}: closest beacon is at x={:d}, y={:d}", line)
    return (res[0], res[1]), (res[2], res[3])


def manhattan(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    data = [process_line(l) for l in read_file(input)]
    target_y = 10 if "ex" in input.name else 2000000

    sensors = set()
    beacons = set()

    for sensor, beacon in data:
        sensors.add(sensor)
        beacons.add(beacon)

    covered = set()
    for sensor, beacon in data:
        d = manhattan(sensor, beacon)
        for target_x in range(sensor[0] - d, sensor[0] + d + 1):
            target = (target_x, target_y)
            if target in sensors or target in beacons:
                continue
            if manhattan(sensor, target) <= d:
                covered.add(target)

    pprint(len(covered))


@cli.command()
@click.argument("input", type=click.File())
def part1_print(input):
    data = [process_line(l) for l in read_file(input)]
    target_y = 10 if "ex" in input.name else 2000000

    grid = GridN(default=".")
    min_x, max_x = maxint, -maxint

    for sensor, beacon in data:
        grid.set(sensor, "S")
        grid.set(beacon, "B")

        d = manhattan(sensor, beacon)
        for x in range(sensor[0] - d, sensor[0] + d + 1):
            for y in range(sensor[1] - d, sensor[1] + d + 1):
                target = (x, y)
                if manhattan(target, sensor) <= d and grid.get(target) == ".":
                    grid.set(target, "#")
                min_x = min(min_x, x)
                max_x = max(max_x, x)

    grid.print()
    pprint(sum(1 for x in range(min_x, max_x + 1) if grid.get((x, target_y)) == "#"))


def range_sub(r, s):
    out = []

    if r[0] < s[0]:
        out.append([r[0], min(s[0], r[1])])

    if s[1] < r[1]:
        out.append([max(s[1], r[0]), r[1]])

    return out


def ranges_sub(rs, s):
    out = []
    for r in rs:
        for x in range_sub(r, s):
            if x:
                out.append(x)
    return out


def ranges_add_point(rs, p):
    out = rs[:]
    extended = False
    if not any(r[0] <= p < r[1] for r in rs):
        out.append([p, p + 1])
    return sorted(out)


def ranges_size(rs):
    return sum(r[1] - r[0] for r in rs)


@cli.command()
@click.argument("input", type=click.File())
def part1_row(input):
    data = [process_line(l) for l in read_file(input)]
    target_y = 10 if "ex" in input.name else 2000000

    row_ranges = [[-target_y * 4, target_y * 4 + 1]]
    start_size = ranges_size(row_ranges)

    for sensor, beacon in data:
        d = manhattan(sensor, beacon)
        sensor_row_width = max(0, d - abs(target_y - sensor[1]))
        if not sensor_row_width:
            continue

        sensor_row_range = [
            sensor[0] - sensor_row_width,
            sensor[0] + sensor_row_width + 1,
        ]

        row_ranges = ranges_sub(row_ranges, sensor_row_range)
        if beacon[1] == target_y:
            row_ranges = ranges_add_point(row_ranges, beacon[0])

    pprint(start_size - ranges_size(row_ranges))


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    data = [process_line(l) for l in read_file(input)]
    max_coord = 20 if "ex" in input.name else 4000000

    beacons = set()

    for target_y in tqdm(range(max_coord)):
        row_ranges = [[0, max_coord + 1]]

        for sensor, beacon in data:
            d = manhattan(sensor, beacon)
            sensor_row_width = max(0, d - abs(target_y - sensor[1]))
            if not sensor_row_width:
                continue

            sensor_row_range = [
                sensor[0] - sensor_row_width,
                sensor[0] + sensor_row_width + 1,
            ]

            row_ranges = ranges_sub(row_ranges, sensor_row_range)
            if beacon[1] == target_y:
                row_ranges = ranges_add_point(row_ranges, beacon[0])
                beacons.add(beacon)

        r = first(r for r in row_ranges if r[1] - r[0] == 1)
        if r:
            the_spot = (r[0], target_y)
            if the_spot not in beacons:
                return print(f"{the_spot} => {the_spot[0] * 4000000 + the_spot[1]}")


if __name__ == "__main__":
    cli()
