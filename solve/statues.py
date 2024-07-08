from collections import Counter
from collections.abc import Iterator
from itertools import chain, permutations, product
from typing import Self

from .positions import *
from .shapes import *


class StatueState:
    """
    Describes the current state of a statue.
    """
    __slots__ = 'alias', 'position', 'own_shape', 'current_shape'

    def __init__(
            self,
            alias: str,
            position: str,
            own_shape: Shape2D,
            current_shape: Shape3D,
            /,
            ) -> None:
        """
        :param alias: Nickname of a person at this statue.
        :param position: Position of this statue.
        :param own_shape: 2D shape assigned to this statue.
        :param current_shape: 3D shape this statue currently holds.
        """
        assert position in POSITIONS, f'room position must be {POSITIONS_MSG}, got {position!r}'
        self.alias = alias
        self.position = position
        self.own_shape = own_shape
        self.current_shape = current_shape

    @property
    def is_done(self, /) -> bool:
        """
        Whether this statue holds 3D shape consisting of 2 different opposite shapes.
        """
        return (
                (
                        self.own_shape == triangle
                        and self.current_shape == cylinder
                )
                or
                (
                        self.own_shape == square
                        and self.current_shape == cone
                )
                or
                (
                        self.own_shape == circle
                        and self.current_shape == prism
                )
        )

    def __eq__(self, other: Self, /) -> bool:
        if isinstance(other, self.__class__):
            return self.position == other.position

        return False

    def __str__(self, /) -> str:
        return self.position

    def __repr__(self, /) -> str:
        return (
            f'{self.__class__.__name__}('
            f'{self.alias!r}, '
            f'{self.position!r}, '
            f'{self.own_shape}, '
            f'{self.current_shape}'
            f')'
        )

    def dissect(self, shape1: Shape2D, other: Self, shape2: Shape2D, /) -> 'DissectMove':
        """
        Dissects this statue with one shape and other statue with other shape
        swapping dissected shapes in affected statues.
        """
        assert shape1 in self.current_shape.terms and shape2 in other.current_shape.terms, (
            'dissecting can be done with 2D shapes which are present in the 3D shape'
        )

        new_self = StatueState(
            self.alias,
            self.position,
            self.own_shape,
            self.current_shape - shape1 + shape2,
            )
        new_other = StatueState(
            other.alias,
            other.position,
            other.own_shape,
            other.current_shape - shape2 + shape1,
            )
        return new_self, shape1, new_other, shape2


type DissectMove = tuple[StatueState, Shape2D, StatueState, Shape2D]


class StateOfAllStatues(StateWithPositions[StatueState, DissectMove]):
    """
    Describes the current state of all statues in the main room in Verity encounter.
    """
    __slots__ = ()

    def make_all_moves(self, /, is_doing_triumph: bool) -> Iterator[Self]:
        """
        Yields all possible next states.
        If argument ``is_doing_triumph`` is ``True``,
        ensures that next moves will not start with the statue dissected last in the last move.
        """
        last_statue = self.moves_made[-1][2] if self.moves_made else None
        for s1, s2, s3 in permutations((self.left, self.middle, self.right)):
            # Do not dissect statue which was dissected last in the last move.
            if is_doing_triumph and last_statue == s1: continue
            # Do nothing if either statue is done
            if s1.is_done or s2.is_done: continue

            for shape1, shape2 in product(s1.current_shape.terms, s2.current_shape.terms):
                # Dissecting the same shapes is useless
                if shape1 == shape2: continue

                # Avoid loops
                # Loop s1 <-> s2
                opposite_move = s1, shape2, s2, shape1
                if opposite_move in self.moves_made:
                    continue

                new_s1, _, new_s2, _ = s1.dissect(shape1, s2, shape2)
                kwargs = {
                    s1.position:  new_s1,
                    s2.position:  new_s2,
                    s3.position:  s3,
                    'moves_made': (*self.moves_made, (s1, shape1, s2, shape2)),
                    }
                yield StateOfAllStatues(**kwargs)

    @property
    def first_position(self, /) -> str:
        return self.moves_made[0][0].position

    @property
    def last_position(self, /) -> str:
        return self.moves_made[-1][2].position


def init_statues(
        left_alias: str,
        left_inner_shape: Shape2D,
        left_held_shape: Shape3D,
        middle_alias: str,
        middle_inner_shape: Shape2D,
        middle_held_shape: Shape3D,
        right_alias: str,
        right_inner_shape: Shape2D,
        right_held_shape: Shape3D,
        ) -> StateOfAllStatues:
    """
    A convenience function to specify the initial state of all statues in the main room.
    """
    inner = left_inner_shape, middle_inner_shape, right_inner_shape
    assert all(isinstance(s, Shape2D) for s in inner), f'all inner shapes must be 2D'
    held = left_held_shape, middle_held_shape, right_held_shape
    assert all(isinstance(s, Shape3D) for s in held), f'all held shapes must be 3D'

    c1 = Counter(inner)
    assert all(v == 1 for v in c1.values()), f'the number of all inner shapes must be 1, got {c1}'
    c2 = Counter(chain.from_iterable(s.terms for s in held))
    assert all(v == 2 for v in c2.values()), \
        f'the number of all 2D terms of held 3D shapes must be 2, got {c2}'

    return StateOfAllStatues(
        StatueState(left_alias, LEFT, left_inner_shape, left_held_shape),
        StatueState(middle_alias, MIDDLE, middle_inner_shape, middle_held_shape),
        StatueState(right_alias, RIGHT, right_inner_shape, right_held_shape),
        )


__all__ = 'init_statues', 'StateOfAllStatues', 'DissectMove'
