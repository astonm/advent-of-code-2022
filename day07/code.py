from util import *


@click.group()
def cli():
    pass


@dataclass
class Directory:
    name: str
    files: dict
    parent: object


@dataclass
class File:
    name: str
    size: int


def get_file_tree(lines):
    root = Directory(name=".", files={}, parent=None)
    i = 0
    while i < len(lines):
        line = lines[i]
        i += 1

        if line == "$ cd /":
            curr_dir = root
        elif line == "$ cd ..":
            curr_dir = curr_dir.parent
            assert curr_dir
        elif line.startswith("$ cd "):
            dir_info = parse("$ cd {}", line)
            curr_dir = curr_dir.files[dir_info[0]]
        elif line.startswith("$ ls"):
            while i < len(lines) and not lines[i].startswith("$"):
                line = lines[i]
                i += 1

                file_info = parse("{:d} {}", line)
                if file_info:
                    new_file = File(file_info[1], file_info[0])
                    curr_dir.files[new_file.name] = new_file

                dir_info = parse("dir {}", line)
                if dir_info:
                    new_dir = Directory(name=dir_info[0], files={}, parent=curr_dir)
                    curr_dir.files[new_dir.name] = new_dir
        else:
            print(f"unexpected command `{line}`")
    return root


def get_dir_sizes(tree):
    out = {}
    my_total = 0
    for file in tree.files.values():
        match file:
            case File():
                my_total += file.size
            case Directory():
                res = get_dir_sizes(file)
                for name, size in res.items():
                    out[tree.name +"/" + name] = size
                my_total += out[tree.name +"/" + file.name]

    out[tree.name] = my_total
    return out


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    root = get_file_tree(read_file(input))
    dir_sizes = get_dir_sizes(root)
    print(sum(s for s in dir_sizes.values() if s <=100000))



@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    root = get_file_tree(read_file(input))
    dir_sizes = get_dir_sizes(root)

    capacity = 70000000
    target_unused = 30000000
    unused = capacity - dir_sizes["."]
    print(min(x for x in dir_sizes.values() if x > (target_unused - unused)))




if __name__ == "__main__":
    cli()
