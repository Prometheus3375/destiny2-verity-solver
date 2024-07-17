from collections.abc import Iterator
from inspect import signature
from typing import Literal, Protocol, Self, TypeGuard

from ..multiset import Multiset
from ..shapes import Shape2D

LEFT: Literal['left'] = 'left'
MIDDLE: Literal['middle'] = 'middle'
RIGHT: Literal['right'] = 'right'
type PositionsType = Literal['left', 'middle', 'right']

_POSITIONS = {LEFT, MIDDLE, RIGHT}
_POSITIONS_MSG = f'{LEFT!r}, {MIDDLE!r} or {RIGHT!r}'


def is_position(s: str, /) -> TypeGuard[PositionsType]:
    """
    Returns ``True`` if a string is a valid position.
    """
    return s in _POSITIONS


class PMove(Protocol):
    @property
    def shape(self, /) -> Shape2D:
        """
        Shape used in this move.
        """

    @property
    def destination(self, /) -> PositionsType:
        """
        Position of this move.
        """


class State:
    """
    Base class for any state.
    """
    __slots__ = 'position', 'own_shape', 'shapes_to_give', 'shapes_to_receive'

    def __init__(
            self,
            /,
            position: PositionsType,
            own_shape: Shape2D,
            shapes_to_give: Multiset[Shape2D],
            shapes_to_receive: Multiset[Shape2D],
            ) -> None:
        assert is_position(position), \
            f'position of a state must be {_POSITIONS_MSG}, got {position!r}'
        self.position = position
        self.own_shape = own_shape
        self.shapes_to_give = shapes_to_give
        self.shapes_to_receive = shapes_to_receive

    @property
    def is_done(self, /) -> bool:
        """
        Whether this state is done.
        """
        return len(self.shapes_to_give) == 0 and len(self.shapes_to_receive) == 0

    @property
    def shapes_available(self, /) -> Multiset[Shape2D]:
        """
        List of shapes available in this state.
        """
        return self.shapes_to_give

    def is_shape_required(self, shape: Shape2D, /) -> bool:
        """
        Return ``True`` if to be done this state requires passed shape.
        """
        return shape in self.shapes_to_receive

    def __repr__(self, /) -> str:
        attrs = ', '.join(f'{attr}={getattr(self, attr)}' for attr in self.__slots__)
        return (
            f'{self.__class__.__name__}('
            f'{self.position.upper()}, '
            f'own_shape={self.own_shape}, '
            f'shapes_to_give={self.shapes_to_give}, '
            f'shapes_to_receive={self.shapes_to_receive}, '
            f'{attrs}'
            f')'
        )


class StateWithAllPositions[S: State, M: PMove]:
    """
    Base class for holding states of positions and moves made.
    """
    __slots__ = 'left', 'middle', 'right', 'moves_made'

    def __init__(self, /, left: S, middle: S, right: S, moves_made: tuple[M, ...] = ()) -> None:
        self.left = left
        self.middle = middle
        self.right = right
        self.moves_made = moves_made

    # region Verify that constructor and slots has POSITIONS
    assert set(__slots__) >= _POSITIONS, f'encounter state must have position attributes'

    signature_ = signature(__init__)
    kwargs = {
        p.name
        for p in signature_.parameters.values()
        if p.kind is p.KEYWORD_ONLY or p.kind is p.POSITIONAL_OR_KEYWORD
        }

    assert kwargs >= _POSITIONS, f'encounter state must have position keyword arguments'
    del signature_, kwargs
    # endregion

    @property
    def is_done(self, /) -> bool:
        """
        Whether states in all positions are done.
        """
        return self.left.is_done and self.middle.is_done and self.right.is_done

    @property
    def first_position(self, /) -> PositionsType:
        """
        First position touched via moves made.
        """
        return self.moves_made[0].destination

    @property
    def last_position(self, /) -> PositionsType:
        """
        Last position touched via moves made.
        """
        return self.moves_made[-1].destination

    def make_all_moves(self, /, is_doing_triumph: bool) -> Iterator[Self]:
        """
        Yields all possible next states.
        """
        raise NotImplementedError

    def __repr__(self, /) -> str:
        return (
            f'{self.__class__.__name__}('
            f'{self.left}, '
            f'{self.middle}, '
            f'{self.right}, '
            f'{self.moves_made}'
            f')'
        )


__all__ = (
    'LEFT',
    'MIDDLE',
    'RIGHT',
    'PositionsType',
    'is_position',
    'State',
    'PMove',
    'StateWithAllPositions',
    )
