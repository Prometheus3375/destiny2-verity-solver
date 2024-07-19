from collections import Counter
from collections.abc import Iterator
from dataclasses import dataclass
from itertools import permutations
from typing import Self

from .base import *
from ..key_sets import KSMixed, KeySetType
from ..multiset import Multiset
from ..shapes import Shape2D


@dataclass(frozen=True, kw_only=True, slots=True)
class PassMove:
    departure: PositionsType
    shape: Shape2D
    destination: PositionsType


class RoomState(State):
    __slots__ = 'dropping_shapes', 'final_dropping_shapes'

    def __init__(
            self,
            position: PositionsType,
            own_shape: Shape2D,
            /,
            *,
            dropping_shapes: Multiset[Shape2D],
            final_dropping_shapes: Multiset[Shape2D],
            shapes_to_receive: Multiset[Shape2D] | None = None,
            ) -> None:
        self.dropping_shapes = dropping_shapes
        self.final_dropping_shapes = final_dropping_shapes
        # Shadow - 2D shape holding by a statue in a room.
        # There are two shadows in each room.
        # For example, circle room has triangle and square shadows.
        # Each solo player must remove shadows to allow everyone to exit.
        # To remove a shadow X, the room must receive shape X.
        # For example, circle room must receive triangle and square to remove both shadows.
        if shapes_to_receive is None:
            # This rooms must receive KSMixed[own_shape].terms in any case.
            # In addition, this room must receive any other shape from final_dropping_shapes
            # unless it is already present in dropping_shapes.
            # Take union (not sum!) between
            # "must receive in any case" and "must receive to be done".
            # Unions of multisets takes the highest count of elements instead of summing count,
            # ex. {triangle, circle} | {triangle, triangle} = {triangle, circle, triangle}.
            shapes_to_receive = KSMixed[own_shape].terms \
                                | (final_dropping_shapes - dropping_shapes)

        super().__init__(
            position=position,
            own_shape=own_shape,
            shapes_to_receive=shapes_to_receive,
            )

    @property
    def is_done(self, /) -> bool:
        return not self.shapes_to_receive and self.dropping_shapes == self.final_dropping_shapes

    @property
    def shapes_available(self, /) -> Multiset[Shape2D]:
        return self.dropping_shapes

    def pass_shape(self, shape: Shape2D, other: Self, /) -> [Self, Self]:
        """
        Transfers a shape from this room to the other.
        Returns two new room states, new self state and new other state.
        """
        new_self = RoomState(
            self.position,
            self.own_shape,
            dropping_shapes=self.dropping_shapes.remove_copy(shape),
            final_dropping_shapes=self.final_dropping_shapes,
            shapes_to_receive=self.shapes_to_receive,
            )
        new_other = RoomState(
            other.position,
            other.own_shape,
            dropping_shapes=other.dropping_shapes.add_copy(shape),
            final_dropping_shapes=other.final_dropping_shapes,
            shapes_to_receive=other.shapes_to_receive.remove_copy(shape),
            )
        return new_self, new_other


class StateOfAllRooms(StateWithAllPositions[RoomState, PassMove]):
    __slots__ = ()

    max_cycles = 9

    def next_states(self, /, is_doing_triumph: bool) -> Iterator[Self]:
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
                        'moves_made': (*self.moves_made, move),
                        }
                    yield StateOfAllRooms(**kwargs)


def init_rooms(
        *,
        left_inner_shape: Shape2D,
        left_other_shape: Shape2D,
        middle_inner_shape: Shape2D,
        middle_other_shape: Shape2D,
        right_inner_shape: Shape2D,
        right_other_shape: Shape2D,
        key_set: KeySetType,
        ) -> StateOfAllRooms:
    """
    A convenience function to specify the initial state of all solo rooms.
    """
    shapes = (
        left_inner_shape,
        left_other_shape,
        middle_inner_shape,
        middle_other_shape,
        right_inner_shape,
        right_other_shape,
        )
    assert all(isinstance(f, Shape2D) for f in shapes), f'all shapes must be 2D shapes'

    c = Counter(shapes)
    assert all(v == 2 for v in c.values()), f'the number of all 2D shapes must be 2, got {c}'

    return StateOfAllRooms(
        left=RoomState(
            LEFT,
            left_inner_shape,
            dropping_shapes=Multiset((left_inner_shape, left_other_shape)),
            final_dropping_shapes=key_set[left_inner_shape].terms,
            ),
        middle=RoomState(
            MIDDLE,
            middle_inner_shape,
            dropping_shapes=Multiset((middle_inner_shape, middle_other_shape)),
            final_dropping_shapes=key_set[middle_inner_shape].terms,
            ),
        right=RoomState(
            RIGHT,
            right_inner_shape,
            dropping_shapes=Multiset((right_inner_shape, right_other_shape)),
            final_dropping_shapes=key_set[right_inner_shape].terms,
            ),
        )


__all__ = 'PassMove', 'StateOfAllRooms', 'init_rooms'
