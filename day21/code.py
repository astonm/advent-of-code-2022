from util import *


@click.group()
def cli():
    pass


@dataclass
class Node:
    val: int = None
    left: any = None
    right: any = None


def process_line(line):
    if m := parse("{name}: {left} {op} {right}", line):
        return m["name"], Node(left=m["left"], val=m["op"], right=m["right"])
    if m := parse("{name}: {val:d}", line):
        return m["name"], Node(val=m["val"])


def build_tree(data, root):
    root = data[root]
    if root.left is None and root.right is None:
        return root

    if isinstance(root.left, str):
        root.left = build_tree(data, root.left)

    if isinstance(root.right, str):
        root.right = build_tree(data, root.right)

    return root


def eval_tree(tree):
    if tree.left is None and tree.right is None:
        return tree.val
    left, right = eval_tree(tree.left), eval_tree(tree.right)
    return {
        "+": lambda: left + right,
        "-": lambda: left - right,
        "*": lambda: left * right,
        "/": lambda: left // right,
    }[tree.val]()


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    data = [process_line(l) for l in read_file(input)]
    nodes = {k: n for (k, n) in data}
    tree = build_tree(nodes, "root")
    print(eval_tree(tree))


def get_expr(tree):
    if tree.left is None and tree.right is None:
        return tree.val

    left, right = get_expr(tree.left), get_expr(tree.right)
    if not all(isinstance(x, int) for x in [left, right]):
        tree.left, tree.right = left, right
        return tree

    return {
        "+": lambda: left + right,
        "-": lambda: left - right,
        "*": lambda: left * right,
        "/": lambda: left // right,
        "=": lambda: (left, right),
    }[tree.val]()


def solve(expr, val):
    if isinstance(expr, int):
        expr, val = val, expr

    while expr != "?":
        if isinstance(expr.left, int):
            val = {  # val = left ~ ?
                "+": lambda: val - expr.left,
                "-": lambda: expr.left - val,
                "*": lambda: val // expr.left,
                "/": lambda: expr.left // val,
            }[expr.val]()
            expr = expr.right
        else:
            assert isinstance(expr.right, int), expr.right
            val = {  # val = ? ~ right
                "+": lambda: val - expr.right,
                "-": lambda: val + expr.right,
                "*": lambda: val // expr.right,
                "/": lambda: expr.right * val,
            }[expr.val]()
            expr = expr.left
    return val


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    data = [process_line(l) for l in read_file(input)]
    nodes = {k: n for (k, n) in data}
    nodes["humn"].val = "?"

    tree = build_tree(nodes, "root")
    expr, val = get_expr(tree.left), get_expr(tree.right)
    print(solve(expr, val))


if __name__ == "__main__":
    cli()
