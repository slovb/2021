def step(template, rules):
    old = template[0]
    polymer = [old]
    for c in template[1::]:
        key = (old, c)
        if key in rules:
            polymer.append(rules[key])
        polymer.append(c)
        old = c
    return polymer


def commonality(polymer):
    counts = {}
    for p in polymer:
        if p not in counts:
            counts[p] = 0
        counts[p] += 1
    return counts


def solve(polymer, rules):
    # print('{}:\t{}'.format(len(polymer), ''.join(polymer)))
    for _ in range(10):
        polymer = step(polymer, rules)
        # print('{}:\t{}'.format(len(polymer), ''.join(polymer)))
    counts = commonality(polymer)
    return max(counts.values()) - min(counts.values())


def read(filename):
    with open(filename, 'r') as f:
        rows = [row.rstrip() for row in f.readlines()]
        template = list(rows[0])
        rules = {}
        for row in rows[2::]:
            left, _, right = row.split(' ')
            rules[(left[0], left[1])] = right
        return template, rules


def main(filename):
    return solve(*read(filename))


if __name__ == "__main__":
    import sys
    if (len(sys.argv) < 2):
        print("\n{}".format(main('input.txt')))
    else:
        for f in sys.argv[1:]:
            print("\n{}".format(main(f)))
