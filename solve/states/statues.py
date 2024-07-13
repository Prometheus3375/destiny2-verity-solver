from collections import Counter
from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from itertools import chain, permutations, product
from typing import Self, Unpack

from .base import *
from ..shapes import *


@dataclass(frozen=True, kw_only=True, slots=True)
class DissectMove:
    shape: Shape2D
    destination: PositionsType


class StatueState(State):
    __slots__ = 'shape_held',

    def __init__(
            self,
            /,
            position: PositionsType,
            own_shape: Shape2D,
            shape_held: Shape3D,
            shapes_to_give: Iterable[Shape2D] | None = None,
            shapes_to_receive: Iterable[Shape2D] | None = None,
            ) -> None:
        required = shape2opposite[own_shape]
        self.shape_held = shape_held

        if shapes_to_give is None:
            shapes_to_give = (
                shape
                for shape in shape_held.terms
                if shape not in required
                )

        if shapes_to_receive is None:
            shapes_to_receive = required.difference(self.shape_held.terms)

        super().__init__(
            position=position,
            own_shape=own_shape,
            shapes_to_give=shapes_to_give,
            shapes_to_receive=shapes_to_receive,
            )

    @property
    def is_done(self, /) -> bool:
        t1, t2 = shape2opposite[self.own_shape]
        return self.shape_held == t1 + t2

    def dissect(self, shape1: Shape2D, other: Self, shape2: Shape2D, /) -> [Self, Self]:
        """
        Dissects this statue with one shape and other statue with other shape
        swapping dissected shapes in affected statues.
        """
        self_to_give = list(self.shapes_to_give)
        self_to_give.remove(shape1)
        self_to_receive = set(self.shapes_to_receive)
        self_to_receive.remove(shape2)

        other_to_give = list(other.shapes_to_give)
        other_to_give.remove(shape2)
        other_to_receive = set(other.shapes_to_receive)
        other_to_receive.remove(shape1)

        new_self = StatueState(
            self.position,
            self.own_shape,
            self.shape_held - shape1 + shape2,
            shapes_to_give=self_to_give,
            shapes_to_receive=self_to_receive,
            )
        new_other = StatueState(
            other.position,
            other.own_shape,
            other.shape_held - shape2 + shape1,
            shapes_to_give=other_to_give,
            shapes_to_receive=other_to_receive,
            )

        return new_self, new_other


class StateOfAllStatues(StateWithAllPositions[StatueState, DissectMove]):
    __slots__ = ()

    def make_all_moves(self, /, is_doing_triumph: bool) -> Iterator[Self]:
        """
        Yields all possible next states.
        If argument ``is_doing_triumph`` is ``True``,
        ensures that next moves will not start with the statue dissected last in the last move.
        """
        last_position = self.last_position if self.moves_made else None
        for s1, s2, s3 in permutations((self.left, self.middle, self.right)):
            # Do not dissect shape from the statue which was dissected in the last move.
            if is_doing_triumph and last_position == s1.position: continue
            # Do nothing if either state is done.
            if s1.is_done or s2.is_done: continue

            for shape1, shape2 in product(s1.shapes_available, s2.shapes_available):
                if s2.is_shape_required(shape1) and s1.is_shape_required(shape2):
                    new_s1, new_s2 = s1.dissect(shape1, s2, shape2)
                    move1 = DissectMove(shape=shape1, destination=s1.position)
                    move2 = DissectMove(shape=shape2, destination=s2.position)
                    kwargs = {
                        s1.position:  new_s1,
                        s2.position:  new_s2,
                        s3.position:  s3,
                        'moves_made': (*self.moves_made, move1, move2)
                        }
                    yield StateOfAllStatues(**kwargs)


class InitStatuesKwargs:
    left_inner_shape: Shape2D
    left_held_shape: Shape3D
    middle_inner_shape: Shape2D
    middle_held_shape: Shape3D
    right_inner_shape: Shape2D
    right_held_shape: Shape3D


def init_statues(**kw: Unpack[InitStatuesKwargs]) -> StateOfAllStatues:
    """
    A convenience function to specify the initial state of all statues in the main room.
    """
    inner = [
        kw[name]
        for name in ('left_inner_shape', 'middle_inner_shape', 'right_inner_shape')
        ]
    assert all(isinstance(s, Shape2D) for s in inner), f'all inner shapes must be 2D'
    held = [
        kw[name]
        for name in ('left_held_shape', 'middle_held_shape', 'right_held_shape')
        ]
    assert all(isinstance(s, Shape3D) for s in held), f'all held shapes must be 3D'

    c1 = Counter(inner)
    assert all(v == 1 for v in c1.values()), f'the number of all inner shapes must be 1, got {c1}'
    c2 = Counter(chain.from_iterable(s.terms for s in held))
    assert all(v == 2 for v in c2.values()), \
        f'the number of all 2D terms of held 3D shapes must be 2, got {c2}'

    return StateOfAllStatues(
        left=StatueState(LEFT, kw['left_inner_shape'], kw['left_held_shape']),
        middle=StatueState(MIDDLE, kw['middle_inner_shape'], kw['middle_held_shape']),
        right=StatueState(RIGHT, kw['right_inner_shape'], kw['right_held_shape']),
        )


__all__ = 'DissectMove', 'StateOfAllStatues', 'InitStatuesKwargs', 'init_statues'
