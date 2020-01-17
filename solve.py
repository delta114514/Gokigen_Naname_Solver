import copy

from enum import Enum
from collections import defaultdict
from itertools import product


class Angle(Enum):
    RIGHT_UP = 0  # ／
    LEFT_UP = 1  # ＼


def check(edge, field):
    assert isinstance(edge, list) and isinstance(field, list)
    assert len(edge) == len(field) + 1

    def check_joint():
        joint_count = [[0 for _ in range(len(edge))] for _ in range(len(edge))]
        for y, column in enumerate(field):
            for x, angle in enumerate(column):
                if angle is Angle.RIGHT_UP:
                    joint_count[y + 1][x] += 1
                    joint_count[y][x + 1] += 1
                elif angle is Angle.LEFT_UP:
                    joint_count[y][x] += 1
                    joint_count[y + 1][x + 1] += 1
        for y, (real_y, max_y) in enumerate(zip(joint_count, edge)):
            for x, (real_x, max_x) in enumerate(zip(real_y, max_y)):
                assert real_x <= max_x

    def check_loop():
        route = defaultdict(set)
        for y, column in enumerate(field):
            for x, angle in enumerate(column):
                if angle is Angle.RIGHT_UP:
                    route[(x, y + 1)] |= {(x + 1, y)}
                    route[(x + 1, y)] |= {(x, y + 1)}
                elif angle is Angle.LEFT_UP:
                    route[(x + 1, y + 1)] |= {(x, y)}
                    route[(x, y)] |= {(x + 1, y + 1)}

        def dfs(start, before=None):
            for next in route[start]:
                if next == before:
                    continue
                if next in visited:
                    raise AssertionError
                visited_all.add(next)
                visited.add(next)
                dfs(next, start)
            return False

        visited_all = set()
        for y in range(len(edge)):
            for x in range(len(edge)):
                if (x, y) not in visited_all:
                    visited = set()
                    dfs((x, y))

    check_joint()
    check_loop()


def initial_set(edge, field):
    for y, column in enumerate(edge):
        for x, num in enumerate(column):
            for x_offset, y_offset in ((-1, 0), (0, 0), (0, -1), (-1, -1)):
                if not 0 <= x + x_offset < len(field) or not 0 <= y + y_offset < len(field):
                    continue
                if num == 0:
                    field[y + y_offset][x + x_offset] = Angle(abs(x_offset + y_offset) % 2)
                elif num == 1 and x in (0, len(edge) - 1) and y in (0, len(edge) - 1):
                    field[max(y - 1, 0)][max(x - 1, 0)] = Angle((y == 0) ^ (x != 0))
                    break
                elif (num == 2 and (x in (0, len(edge) - 1) or y in (0, len(edge) - 1))) or num == 4:
                    field[y + y_offset][x + x_offset] = Angle(
                        abs(x_offset + y_offset + 1) % 2)


def match(edge, field):
    changed = False
    for y, column in enumerate(edge):
        for x, num in enumerate(column):
            c_count = 0
            not_touch = 0
            for x_offset, y_offset in ((-1, 0), (0, 0), (0, -1), (-1, -1)):
                if not 0 <= x + x_offset < len(field) or not 0 <= y + y_offset < len(field):
                    continue
                cx, cy = x + x_offset, y + y_offset
                c_count += field[cy][cx] is Angle(abs(x_offset + y_offset + 1) % 2)
                not_touch += field[cy][cx] is Angle(abs(x_offset + y_offset) % 2)
            if c_count == edge[y][x]:
                for x_offset, y_offset in ((-1, 0), (0, 0), (0, -1), (-1, -1)):
                    if not 0 <= x + x_offset < len(field) or not 0 <= y + y_offset < len(
                            field):
                        continue
                    cx, cy = x + x_offset, y + y_offset
                    if field[cy][cx] is None:
                        field[cy][cx] = Angle(abs(x_offset + y_offset) % 2)
                        changed = True
            if not_touch == 4 - edge[y][x]:
                for x_offset, y_offset in ((-1, 0), (0, 0), (0, -1), (-1, -1)):
                    if not 0 <= x + x_offset < len(field) or not 0 <= y + y_offset < len(
                            field):
                        continue
                    cx, cy = x + x_offset, y + y_offset
                    if field[cy][cx] is None:
                        field[cy][cx] = Angle(abs(x_offset + y_offset + 1) % 2)
                        changed = True
    return changed


def pretty_print(field):
    length = len(field)
    print("-" * (1 + 2 * length))
    for col in field:
        print("|{}|".format("".join(
            map(
                lambda x: "／" if x is Angle.RIGHT_UP else "＼" if x is not None else "  ",
                col))))
    print("-" * (1 + 2 * length))


def not_filled(field):
    no_fill = set()
    for y, col in enumerate(field):
        for x, val in enumerate(col):
            if val is None:
                no_fill.add((y, x))
    return no_fill


def solve(edge):
    around_edge = set()
    for y, col in enumerate(edge):
        for x, val in enumerate(col):
            if val < 0:
                edge[y][x] = float('inf')
            else:
                for y_offset, x_offset in product((-1, 0), (-1, 0)):
                    if not 0 <= x + x_offset < len(edge) + 1 or not 0 <= y + y_offset < len(edge) + 1:
                        continue
                    around_edge.add((x + x_offset, y + y_offset))

    assert all((len(x) == len(edge[0]) for x in edge))
    field = [[None for _ in range(len(edge[0]) - 1)]
             for _ in range(len(edge[0]) - 1)]
    check(edge, field)
    initial_set(edge, field)
    stack = []

    def new_stack():
        def get_next_pos():
            not_filled_pos = around_edge & not_filled(field)
            if not_filled_pos:
                return not_filled_pos.pop()
            else:
                for y, column in enumerate(field):
                    for x, num in enumerate(column):
                        if num is None:
                            return y, x
            return None, None

        y, x = get_next_pos()
        if y is x is None:
            return
        extended = False
        new_field_0 = copy.deepcopy(field)
        new_field_1 = copy.deepcopy(field)
        try:
            new_field_0[y][x] = Angle(0)
            check(edge, new_field_0)
            stack.extend([new_field_0])
            extended = True
        except AssertionError:
            pass
        try:
            new_field_1[y][x] = Angle(1)
            check(edge, new_field_1)
            stack.extend([new_field_1])
            extended = True
        except AssertionError:
            pass
        if extended:
            return

    while any(None in y for y in field):
        if stack:
            field = stack.pop()
        while match(edge, field):
            pass
        new_stack()

    return field


if __name__ == "__main__":
    size = int(input("size of board: "))
    edge = [
        list(map(int, input(f"{n}th line").replace(" ", "5")))
        for n in range(size + 1)
    ]
    field = solve(edge)
    pretty_print(field)
