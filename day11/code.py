from util import *


@click.group()
def cli():
    pass


@dataclass
class Monkey:
    items: list = None
    op: str = ""
    divisor: int = 0
    pass_to: list = field(default_factory=lambda: [0, 0])


def process_line(spec):
    monkey = Monkey()
    for line in spec.splitlines():
        line = line.strip()
        if m := parse("Starting items: {}", line):
            items = [int(x) for x in m[0].split(", ")]
        if m := parse("Operation: {}", line):
            op = m[0].replace("new = ", "")
        if m := parse("Test: divisible by {:d}", line):
            divisor = m[0]
        if m := parse("If true: throw to monkey {:d}", line):
            pass_true = m[0]
        if m := parse("If false: throw to monkey {:d}", line):
            pass_false = m[0]
    return Monkey(items, op, divisor, [pass_false, pass_true])


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    monkeys = [process_line(l) for l in read_file(input, delim="\n\n")]
    num_inspected = Counter()
    for round in range(20):
        for i, monkey in enumerate(monkeys):
            if not monkey.items:
                continue
            while monkey.items:
                worry = monkey.items.pop(0)
                num_inspected[i] += 1
                worry = eval(monkey.op, {"old": worry}) // 3
                next_monkey = monkey.pass_to[worry % monkey.divisor == 0]
                monkeys[next_monkey].items.append(worry)

    pprint(prod(x[1] for x in num_inspected.most_common(2)))


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    monkeys = [process_line(l) for l in read_file(input, delim="\n\n")]
    all_divisors = prod(m.divisor for m in monkeys)

    num_inspected = Counter()
    for round in range(10000):
        for i, monkey in enumerate(monkeys):
            if not monkey.items:
                continue
            while monkey.items:
                worry = monkey.items.pop(0)
                num_inspected[i] += 1
                worry = eval(monkey.op, {"old": worry})

                next_monkey = monkey.pass_to[worry % monkey.divisor == 0]
                next_worry = worry % all_divisors
                monkeys[next_monkey].items.append(worry % all_divisors)

    pprint(prod(x[1] for x in num_inspected.most_common(2)))


if __name__ == "__main__":
    cli()
