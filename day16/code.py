from util import *


@click.group()
def cli():
    pass


def process_line(line):
    singular = "Valve {} has flow rate={:d}; tunnel leads to valve {}"
    plural = "Valve {} has flow rate={:d}; tunnels lead to valves {}"
    res = parse(singular, line) or parse(plural, line)
    return (res[0], res[1], res[2].split(", "))


def distance(g, start, end, seen=tuple(), cache={}):
    if start == end:
        return 0

    if end in g[start]:
        return 1

    seen = seen + (start,)

    possibles = [x for x in g[start] if x not in seen]
    if not possibles:
        return 1000000

    d = 1 + min(distance(g, n, end, seen) for n in possibles)
    return d


def get_paths(graph, rates):
    initial_on_valves = {v: 30 for (v, r) in rates.items() if r == 0}
    start = ("AA", 30, initial_on_valves)
    q = [start]
    dist_cache = {}

    def dist(s, e):
        p = (s, e)
        if p not in dist_cache:
            dist_cache[p] = distance(graph, *p)
        return dist_cache[p]

    while q:
        curr, time_left, on_valves = q.pop()
        others_to_try = set(graph) - set(on_valves)

        added_paths = False
        for next_valve in others_to_try:
            turn_on_time = dist(curr, next_valve) + 1
            if time_left >= turn_on_time:
                next_time = time_left - turn_on_time
                next_valves = on_valves.copy()
                next_valves[next_valve] = next_time
                q.append((next_valve, next_time, next_valves))
                added_paths = True

        if not added_paths:
            yield on_valves


def score_path(path, rates):
    return sum(rates[v] * t for (v, t) in path.items())


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    data = [process_line(l) for l in read_file(input)]

    graph = {}
    rates = {}
    for valve, rate, adjacent in data:
        graph[valve] = adjacent
        rates[valve] = rate

    print(max(score_path(p, rates) for p in get_paths(graph, rates)))


def get_paths_two(graph, rates):
    initial_on_valves = {v: 26 for (v, r) in rates.items() if r == 0}
    start = (("AA", 26), ("AA", 26), initial_on_valves)
    q = [start]
    dist_cache = {}

    best_for = defaultdict(int)

    def dist(s, e):
        p = (s, e)
        if p not in dist_cache:
            dist_cache[p] = distance(graph, *p)
        return dist_cache[p]

    while q:
        person, elephant, on_valves = q.pop()

        # more aggressive pruning
        progress = tuple(sorted(on_valves))
        progress_score = score_path(on_valves, rates)
        if best_for[progress] > progress_score:
            continue
        else:
            best_for[progress] = progress_score

        added_paths = False
        others_to_try = set(graph) - set(on_valves)
        for next_valve in others_to_try:
            for i, (curr, time_left) in enumerate([person, elephant]):
                turn_on_time = dist(curr, next_valve) + 1
                if time_left >= turn_on_time:
                    next_time = time_left - turn_on_time
                    next_valves = on_valves.copy()
                    next_valves[next_valve] = next_time

                    next_person = (next_valve, next_time) if i == 0 else person
                    next_elephant = (next_valve, next_time) if i == 1 else elephant
                    q.append((next_person, next_elephant, next_valves))
                    added_paths = True

        if not added_paths:
            yield on_valves


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    data = [process_line(l) for l in read_file(input)]

    graph = {}
    rates = {}
    for valve, rate, adjacent in data:
        graph[valve] = adjacent
        rates[valve] = rate

    print(max(score_path(p, rates) for p in get_paths_two(graph, rates)))


if __name__ == "__main__":
    cli()
