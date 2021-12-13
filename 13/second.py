def execute(dots, along, at):
    output = []
    for x, y in dots:
        extra = None
        if along == 'x':
            if x <= at:
                extra = (x, y)
            else:
                extra = (2*at - x, y)
        elif along == 'y':
            if y <= at:
                extra = (x, y)
            else:
                extra = (x, 2*at - y)
        else:
            raise Exception('error')
        if extra not in output:
            output.append(extra)
    return output


def display(dots):
    max_x = max([x for x, _ in dots])
    max_y = max([y for _, y in dots])
    rows = []
    for y in range(max_y + 1):
        row = []
        for x in range(max_x + 1):
            if (x, y) in dots:
                row.append('#')
            else:
                row.append('.')
        rows.append(''.join(row))
    return '\n'.join(rows)


def solve(dots, folds):
    # print(display(dots))
    print(len(dots))
    for along, at in folds:
        dots = execute(dots, along, at)
        print()
        print('fold along {} = {}'.format(along, at))
        # print(display(dots))
        print(len(dots))
    print(display(dots))
    return len(dots)


def read(filename):
    with open(filename, 'r') as f:
        rows = [row.rstrip() for row in f.readlines()]
        dots = []
        folds = []
        i = 0
        while rows[i] != '':
            dots.append(tuple([int(n) for n in rows[i].split(',')]))
            
            i += 1
        for row in rows[i+1::]:
            fold = row.split(' ')[2].split('=')
            folds.append((fold[0], int(fold[1])))
        return dots, folds


def main(filename):
    return solve(*read(filename))


if __name__ == "__main__":
    import sys
    if (len(sys.argv) < 2):
        print("\n{}".format(main('input.txt')))
    else:
        for f in sys.argv[1:]:
            print("\n{}".format(main(f)))
