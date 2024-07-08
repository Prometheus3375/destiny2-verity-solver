from solve.shapes import *
from solve.solver import solve_encounter


def main():
    TRIUMPH = True
    aliases = 'A', 'B', 'C'
    inner = circle, triangle, square
    other = circle, triangle, square
    held = sphere, pyramid, cube

    m1, m2 = solve_encounter(
        left_alias=aliases[0],
        middle_alias=aliases[1],
        right_alias=aliases[2],
        left_inner_shape=inner[0],
        middle_inner_shape=inner[1],
        right_inner_shape=inner[2],
        left_other_shape=other[0],
        middle_other_shape=other[1],
        right_other_shape=other[2],
        left_held_shape=held[0],
        middle_held_shape=held[1],
        right_held_shape=held[2],
        is_doing_triumph=TRIUMPH,
        )

    print('Start with solo rooms')
    for r1, shape, r2 in m1:
        _ = input(f'Player {r1.alias} ({r1.position}): pass {shape} to {r2.position}')

    print(
        '--- SOLO ROOMS ARE DONE ---\n'
        'All player in the solo rooms must collect two shapes and wait\n'
        'Proceed with dissection\n'
        )

    for s1, shape1, s2, shape2 in m2:
        _ = input(f'Dissect {shape1} from {s1.position}')
        _ = input(f'Dissect {shape2} from {s2.position}')

    print(
        '--- DISSECTION IS DONE ---\n'
        'All players in the solo rooms must leave them'
        )


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
