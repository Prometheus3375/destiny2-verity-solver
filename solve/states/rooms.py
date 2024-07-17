from collections import Counter
from collections.abc import Iterator
from dataclasses import dataclass
from itertools import permutations
from typing import Self, TypedDict, Unpack

from .base import *
from ..multiset import Multiset
from ..shapes import *


@dataclass(frozen=True, kw_only=True, slots=True)
class PassMove:
    departure: PositionsType
    shape: Shape2D
    destination: PositionsType


class RoomState(State):
    __slots__ = 'dropping_shapes',

    def __init__(
            self,
            /,
            position: PositionsType,
            own_shape: Shape2D,
            dropping_shapes: Multiset[Shape2D],
            shapes_to_give: Multiset[Shape2D] | None = None,
            shapes_to_receive: Multiset[Shape2D] | None = None,
            ) -> None:
        self.dropping_shapes = dropping_shapes
        shapes_to_give = self.dropping_shapes if shapes_to_give is None else shapes_to_give
        shapes_to_receive = (
            shape2opposite[own_shape] if shapes_to_receive is None
            else shapes_to_receive
        )
        super().__init__(
            position=position,
            own_shape=own_shape,
            shapes_to_give=shapes_to_give,
            shapes_to_receive=shapes_to_receive,
            )

    @property
    def is_done(self, /) -> bool:
        """
        Whether this room contains exactly 2 different opposite shapes
        and none of dropping shapes must be given.
        """
        return (
                not self.shapes_to_give
                and len(drops := set(self.dropping_shapes)) == 2
                and drops == shape2opposite[self.own_shape]
        )

    def pass_shape(self, shape: Shape2D, other: Self, /) -> [Self, Self]:
        """
        Transfers a shape from this room to the other.
        Returns two new room states, new self state and new other state.
        """
        new_self = RoomState(
            self.position,
            self.own_shape,
            dropping_shapes=self.dropping_shapes.remove_copy(shape),
            shapes_to_give=self.shapes_to_give.remove_copy(shape),
            shapes_to_receive=self.shapes_to_receive,
            )
        new_other = RoomState(
            other.position,
            other.own_shape,
            dropping_shapes=other.dropping_shapes.add_copy(shape),
            shapes_to_give=other.shapes_to_give,
            shapes_to_receive=other.shapes_to_receive.remove_copy(shape),
            )
        return new_self, new_other


class StateOfAllRooms(StateWithAllPositions[RoomState, PassMove]):
    __slots__ = ()

    def make_all_moves(self, /, is_doing_triumph: bool) -> Iterator[Self]:
        """
        Yields all possible next states.
        If argument ``is_doing_triumph`` is ``True``,
        ensures that next moves will not pass shape the room received shape in the last step.
        """
        last_position = self.last_position if self.moves_made else None
        for s1, s2, s3 in permutations((self.left, self.middle, self.right)):
            # Do not pass shape to the room which was a receiver in the last move.
            if is_doing_triumph and last_position == s2.position: continue
            # Do nothing if either state is done.
            if s1.is_done or s2.is_done: continue

            for shape in s1.shapes_available:
                if s2.is_shape_required(shape):
                    new_s1, new_s2 = s1.pass_shape(shape, s2)
                    move = PassMove(departure=s1.position, shape=shape, destination=s2.position)
                    kwargs = {
                        s1.position:  new_s1,
                        s2.position:  new_s2,
                        s3.position:  s3,
                        'moves_made': (*self.moves_made, move)
                        }
                    yield StateOfAllRooms(**kwargs)


class InitRoomsKwargs(TypedDict):
    left_inner_shape: Shape2D
    left_other_shape: Shape2D
    middle_inner_shape: Shape2D
    middle_other_shape: Shape2D
    right_inner_shape: Shape2D
    right_other_shape: Shape2D


def init_rooms(**kw: Unpack[InitRoomsKwargs]) -> StateOfAllRooms:
    """
    A convenience function to specify the initial state of all solo rooms.
    """
    shapes = kw.values()
    assert all(isinstance(f, Shape2D) for f in shapes), f'all shapes must be 2D shapes'

    c = Counter(shapes)
    assert all(v == 2 for v in c.values()), f'the number of all 2D shapes must be 2, got {c}'

    return StateOfAllRooms(
        left=RoomState(
            LEFT,
            kw['left_inner_shape'],
            Multiset((kw['left_inner_shape'], kw['left_other_shape'])),
            ),
        middle=RoomState(
            MIDDLE,
            kw['middle_inner_shape'],
            Multiset((kw['middle_inner_shape'], kw['middle_other_shape'])),
            ),
        right=RoomState(
            RIGHT,
            kw['right_inner_shape'],
            Multiset((kw['right_inner_shape'], kw['right_other_shape'])),
            ),
        )


__all__ = 'PassMove', 'StateOfAllRooms', 'InitRoomsKwargs', 'init_rooms'
