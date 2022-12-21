from util import *


@click.group()
def cli():
    pass


def process_line(line):
    r = parse(
        (
            "Blueprint {:d}: "
            "Each ore robot costs {:d} ore. "
            "Each clay robot costs {:d} ore. "
            "Each obsidian robot costs {:d} ore and {:d} clay. "
            "Each geode robot costs {:d} ore and {:d} obsidian."
        ),
        line,
    )
    return {
        "ore": [("ore", r[1])],
        "clay": [("ore", r[2])],
        "obsidian": [("ore", r[3]), ("clay", r[4])],
        "geode": [("ore", r[5]), ("obsidian", r[6])],
    }


@dataclass
class State:
    have: dict
    bots: dict
    tick: int = 0

    def buy(self, item, costs, dt):
        # run through previously elapsed time
        state = self.run(dt)

        for r, n in costs:
            assert n <= state.have[r], f"fail buying {item} at tick {self.tick}"
            state.have[r] -= n

        # run one more cycle after buying
        state = state.run(1)

        # built item
        state.bots[item] += 1

        return state

    def run(self, dt):
        bots = self.bots.copy()
        have = self.have.copy()
        tick = self.tick

        for r in self.bots:
            have[r] += self.bots[r] * dt
        tick += dt

        return State(have=have, bots=bots, tick=tick)

    def finish(self, last_tick):
        dt = last_tick - self.tick
        return self.run(dt)


def time_to_buy(item, state, cost):
    if all(n <= state.have[r] for (r, n) in cost[item]):
        return 0

    freqs = []
    for r, n in cost[item]:
        if n > state.have[r]:
            n_left = n - state.have[r]
            n_bots = state.bots[r]
            freqs.append(n_bots / n_left)

    slowest = min(freqs)
    if slowest == 0:
        return None
    else:
        return int(ceil(1 / slowest))


def max_geodes(cost, time_limit):
    start = State(
        bots={
            "ore": 1,
            "clay": 0,
            "obsidian": 0,
            "geode": 0,
        },
        have={
            "ore": 0,
            "clay": 0,
            "obsidian": 0,
            "geode": 0,
        },
    )

    q = [start]
    best_geodes = 0
    min_geode_buys = defaultdict(lambda: maxint)
    while q:
        curr = q.pop()
        if curr.tick >= time_limit:
            before = best_geodes
            best_geodes = max(best_geodes, curr.have["geode"])
            continue

        n_geode_bots = curr.bots["geode"]
        if curr.tick > min_geode_buys[n_geode_bots + 1]:
            continue
        min_geode_buys[n_geode_bots] = min(min_geode_buys[n_geode_bots], curr.tick)

        bought = False
        for item, prices in cost.items():
            next_time = time_to_buy(item, curr, cost)
            if next_time is None:
                continue
            if curr.tick + next_time < time_limit:
                next_state = curr.buy(item, prices, next_time)
                q.append(next_state)
                bought = True

        if not bought:
            q.append(curr.finish(time_limit))

    return best_geodes


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    data = list(enumerate([process_line(l) for l in read_file(input)], start=1))
    print(sum(i * max_geodes(cost, 24) for i, cost in tqdm(data)))


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    data = [process_line(l) for l in read_file(input)][:3]
    print(prod(max_geodes(cost, 32) for cost in tqdm(data)))


if __name__ == "__main__":
    cli()
