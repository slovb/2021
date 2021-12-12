bold = lambda s: '\033[1m{}\033[0m'.format(s)


class Node:
    def __init__(self, name):
        self.name = name
        self.is_big = name.isupper()
        self.neighbours = []
    
    def __str__(self) -> str:
        return '{}: {}'.format(
            self.name if not self.is_big else bold(self.name),
            ', '.join([n.name for n in self.neighbours])
        )


def traverse(current: Node, goal: Node, memory=[], has_revisited = False):
    if current == goal:
        return 1
    if not current.is_big:
        memory.append(current)
    total = 0
    for n in current.neighbours:
        if n.name == 'start':
            continue
        if n in memory:
            if not has_revisited:
                total += traverse(n, goal, memory.copy(), True)
        else:
            total += traverse(n, goal, memory.copy(), has_revisited)
    return total
    

def solve(network):
    start = network['start']
    end = network['end']
    return traverse(start, end)


def read(filename):
    with open(filename, 'r') as f:
        rows = [row.rstrip().split('-') for row in f.readlines()]
        network = {}
        for left, right in rows:
            if left not in network:
                network[left] = Node(left)
            if right not in network:
                network[right] = Node(right)
            network[left].neighbours.append(network[right])
            network[right].neighbours.append(network[left])
        return network


def main(filename):
    return solve(read(filename))


if __name__ == "__main__":
    import sys
    if (len(sys.argv) < 2):
        print("\n{}".format(main('input.txt')))
    else:
        for f in sys.argv[1:]:
            print("\n{}".format(main(f)))
