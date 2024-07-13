from dataclasses import dataclass

from solve.shapes import *
from solve.solver import solve_encounter
from solve.states import LEFT, MIDDLE, RIGHT

T = triangle
C = circle
S = square

CC = sphere
CT = cone
CS = cylinder
TT = pyramid
TS = prism
SS = cube

L = LEFT
M = MIDDLE
R = RIGHT


@dataclass(slots=True, frozen=True)
class Person:
    alias: str
    their_shape: Shape2D
    other_shape: Shape2D


def main():
    triumph = True

    inner = triangle, circle, square,
    person1 = Person(
        alias='A',
        their_shape=T,
        other_shape=T,
        )
    person2 = Person(
        alias='B',
        their_shape=S,
        other_shape=S,
        )
    person3 = Person(
        alias='C',
        their_shape=C,
        other_shape=C,
        )
    held = CT, CT, SS

    lp = LEFT
    lp = MIDDLE
    lp = RIGHT
    lp = None

    inner2person = {
        i: p
        for i in inner
        for p in (person1, person2, person3)
        if p.their_shape == i
        }
    aliases = dict(zip((LEFT, MIDDLE, RIGHT), (inner2person[i].alias for i in inner)))
    other = tuple(inner2person[i].other_shape for i in inner)

    pass_moves, dissect_moves, lp = solve_encounter(
        left_inner_shape=inner[0],
        middle_inner_shape=inner[1],
        right_inner_shape=inner[2],
        left_other_shape=other[0],
        middle_other_shape=other[1],
        right_other_shape=other[2],
        left_held_shape=held[0],
        middle_held_shape=held[1],
        right_held_shape=held[2],
        is_doing_triumph=triumph,
        last_position=lp,
        )

    print('Start with solo rooms')
    for m in pass_moves:
        _ = input(
            f'Player {aliases[m.departure]} ({m.departure}): '
            f'pass {m.shape} to {m.destination}'
            )

    print(
        '--- SOLO ROOMS ARE DONE ---\n'
        'All player in the solo rooms must collect two shapes and wait\n'
        'Proceed with dissection\n'
        )

    for m in dissect_moves:
        _ = input(f'Dissect {m.shape} from {m.destination}')

    print(
        '--- DISSECTION IS DONE ---\n'
        'All players in the solo rooms must leave them\n'
        '--- LAST POSITION ---\n'
        f'{lp.upper()}'
        )


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
