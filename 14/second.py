def step(polymer, rules):
    neu = {}
    def add(key, val):
        if key not in neu:
            neu[key] = 0
        neu[key] += val
    for p, n in polymer.items():
        if p in rules:
            insert = rules[p]
            add(p[0] + insert, n)
            add(insert + p[1], n)
        else:
            add(p, n)
    return neu


def commonality(polymer, first, last):
    counts = {}
    def add(c, n):
        if c not in counts:
            counts[c] = 0
        counts[c] += n
    for p, n in polymer.items():
        add(p[0], n)
        add(p[1], n)
    # everything but the first and last gets doublecounted so add one of each of those and halve all
    counts[first] += 1
    counts[last] += 1
    return {key: count//2 for key, count in counts.items()}


def solve(polymer, rules, first, last):
    for i in range(40):
        polymer = step(polymer, rules)
        # print(polymer)
        # print('{}: {}'.format(i, sum([polymer[p] for p in polymer])))
    counts = commonality(polymer, first, last)
    return max(counts.values()) - min(counts.values())


def read(filename):
    with open(filename, 'r') as f:
        rows = [row.rstrip() for row in f.readlines()]
        template = rows[0]
        polymer = {}
        prev = template[0]
        for c in template[1::]:
            p = prev + c
            if p not in polymer:
                polymer[p] = 0
            polymer[p] += 1
            prev = c
        rules = {}
        for row in rows[2::]:
            left, _, right = row.split(' ')
            rules[left] = right
        return polymer, rules, template[0], template[-1]


def main(filename):
    return solve(*read(filename))


if __name__ == "__main__":
    import sys
    if (len(sys.argv) < 2):
        print("\n{}".format(main('input.txt')))
    else:
        for f in sys.argv[1:]:
            print("\n{}".format(main(f)))
