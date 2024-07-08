from collections import Counter
from collections.abc import Iterator
from itertools import permutations
from typing import Self

from .positions import *
from .shapes import Shape2D, circle, square, triangle


class RoomState:
    """
    Describes the current state of a room.
    """
    __slots__ = 'alias', 'position', 'own_shape', 'present_shapes'

    def __init__(
            self,
            alias: str,
            position: str,
            own_shape: Shape2D,
            /,
            *present_shapes: Shape2D,
            ) -> None:
        """
        :param alias: Nickname of a person in this room.
        :param position: Position of this room.
        :param own_shape: 2D shape assigned to this room.
        :param present_shapes: Shapes in the room that can be collected by defeating knights.
        """
        assert position in POSITIONS, f'room position must be {POSITIONS_MSG}, got {position!r}'
        self.alias = alias
        self.position = position
        self.own_shape = own_shape
        self.present_shapes = present_shapes

    @property
    def is_done(self, /) -> bool:
        """
        Whether this room contains 2 different opposite shapes.
        """
        return (
                len(self.present_shapes) == 2
                and
                (
                        (
                                self.own_shape == triangle
                                and circle in self.present_shapes
                                and square in self.present_shapes
                        )
                        or
                        (
                                self.own_shape == square
                                and triangle in self.present_shapes
                                and circle in self.present_shapes
                        )
                        or
                        (
                                self.own_shape == circle
                                and triangle in self.present_shapes
                                and square in self.present_shapes
                        )
                )
        )

    def __eq__(self, other: Self, /) -> bool:
        if isinstance(other, self.__class__):
            return self.position == other.position

        return False

    def __str__(self, /) -> str:
        return self.position

    def __repr__(self, /) -> str:
        if self.present_shapes:
            args = f', {', '.join(map(str, self.present_shapes))}'
        else:
            args = ''

        return (
            f'{self.__class__.__name__}('
            f'{self.alias!r}, '
            f'{self.position!r}, '
            f'{self.own_shape}{args}'
            f')'
        )

    def pass_shape(self, shape: Shape2D, other: Self, /) -> 'PassMove':
        """
        Passes a 2D shape from this room to another.
        """
        assert shape in self.present_shapes, f'{shape} is not present in {self.position} room'

        li = list(self.present_shapes)
        li.remove(shape)
        new_self = RoomState(
            self.alias,
            self.position,
            self.own_shape,
            *li,
            )
        new_other = RoomState(
            other.alias,
            other.position,
            other.own_shape,
            *other.present_shapes,
            shape,
            )

        return new_self, shape, new_other


type PassMove = tuple[RoomState, Shape2D, RoomState]


class StateOfAllRooms(StateWithPositions[RoomState, PassMove]):
    """
    Describes the current state of all solo rooms in Verity encounter.
    """
    __slots__ = ()

    def make_all_moves(self, /, is_doing_triumph: bool) -> Iterator[Self]:
        """
        Yields all possible next states.
        If argument ``is_doing_triumph`` is ``True``,
        ensures that next moves will not pass shape the room received shape in the last step.
        """
        last_room = self.moves_made[-1][2] if self.moves_made else None
        for r1, r2, r3 in permutations((self.left, self.middle, self.right)):
            # Do not pass shape to the room which was a receiver in the last move.
            if is_doing_triumph and last_room == r2: continue
            # Do nothing if either room is done
            if r1.is_done or r2.is_done: continue

            for shape in r1.present_shapes:
                # Avoid loops in moves
                # Loop r2 -> r1 -> r2
                opposite_move = r2, shape, r1
                if opposite_move in self.moves_made:
                    continue

                # Loop r2 -> r3 -> r1 -> r2
                loop_move1 = r2, shape, r3
                loop_move2 = r3, shape, r1
                if loop_move1 in self.moves_made and loop_move2 in self.moves_made:
                    continue

                # Move r1 -> r2 will not create a loop
                new_r1, _, new_r2 = r1.pass_shape(shape, r2)
                kwargs = {
                    r1.position:  new_r1,
                    r2.position:  new_r2,
                    r3.position:  r3,
                    'moves_made': (*self.moves_made, (r1, shape, r2))
                    }
                yield StateOfAllRooms(**kwargs)

    @property
    def first_position(self, /) -> str:
        return self.moves_made[0][2].position

    @property
    def last_position(self, /) -> str:
        return self.moves_made[-1][2].position


def init_rooms(
        left_alias: str,
        left_shape: Shape2D,
        left_other_shape: Shape2D,
        middle_alias: str,
        middle_shape: Shape2D,
        middle_other_shape: Shape2D,
        right_alias: str,
        right_shape: Shape2D,
        right_other_shape: Shape2D,
        ) -> StateOfAllRooms:
    """
    A convenience function to specify the initial state of all solo rooms.
    """
    shapes = (
        left_shape,
        left_other_shape,
        middle_shape,
        middle_other_shape,
        right_shape,
        right_other_shape,
        )
    assert all(isinstance(f, Shape2D) for f in shapes), f'all shapes must be 2D shapes'

    c = Counter(shapes)
    assert all(v == 2 for v in c.values()), f'the number of all 2D shapes must be 2, got {c}'

    return StateOfAllRooms(
        RoomState(left_alias, LEFT, left_shape, left_shape, left_other_shape),
        RoomState(middle_alias, MIDDLE, middle_shape, middle_shape, middle_other_shape),
        RoomState(right_alias, RIGHT, right_shape, right_shape, right_other_shape),
        )


__all__ = 'init_rooms', 'StateOfAllRooms', 'PassMove'
