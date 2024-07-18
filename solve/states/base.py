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
    __slots__ = 'position', 'own_shape', '_shapes_to_give', '_shapes_to_receive'
    def __init_subclass__(cls, /) -> None:
        cls.__all_slots__ = slots = frozenset(
            slot
            for klass in cls.mro()
            for slot in klass.__dict__.get('__slots__') or ()
            )

        parameters = dict(signature(cls).parameters)
        if not (slots >= parameters.keys()):
            raise TypeError(
                f'slots of class {cls.__name__!r} must include '
                f'parameters of its constructor'
                )

        cls.__positional_slots__ = tuple(
            name
            for name, p in parameters.items()
            if p.kind == p.POSITIONAL_ONLY
            )
        cls.__keyword_slots__ = tuple(
            name
            for name, p in parameters.items()
            if p.kind == p.POSITIONAL_OR_KEYWORD or p.kind == p.KEYWORD_ONLY
            )

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
        self._shapes_to_give = shapes_to_give
        self._shapes_to_receive = shapes_to_receive

    @property
    def is_done(self, /) -> bool:
        """
        Whether this state is done.
        """
        return len(self._shapes_to_give) == 0 and len(self._shapes_to_receive) == 0

    @property
    def shapes_to_give(self, /) -> Multiset[Shape2D]:
        """
        The multiset of shapes which should be given to other states.
        """
        return self._shapes_to_give

    def is_shape_required(self, shape: Shape2D, /) -> bool:
        """
        Return ``True`` if the given shape is required for this state to be done.
        """
        return shape in self._shapes_to_receive

    def __repr__(self, /) -> str:
        positional = ', '.join(f'{getattr(self, attr)!r}' for attr in self.__positional_slots__)
        keyword = ', '.join(f'{attr}={getattr(self, attr)!r}' for attr in self.__keyword_slots__)
        args = ', '.join((positional, keyword))
        return f'{self.__class__.__name__}({args})'


class StateWithAllPositions[S: State, M: PMove]:
    """
    Base class for holding states of positions and moves made.
    """
    __slots__ = 'left', 'middle', 'right', 'moves_made'

    max_cycles: int
    """
    The maximum number of cycles to solve states of this type.
    """

    def __init__(self, /, left: S, middle: S, right: S, moves_made: tuple[M, ...] = ()) -> None:
        self.left = left
        self.middle = middle
        self.right = right
        self.moves_made = moves_made

    # region Verify that constructor and slots have POSITIONS
    assert set(__slots__) >= _POSITIONS, f'encounter state must have position attributes'

    signature_ = signature(__init__)
    kwargs = {
        p.name
        for p in signature_.parameters.values()
        if p.kind == p.KEYWORD_ONLY or p.kind == p.POSITIONAL_OR_KEYWORD
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

    def next_states(self, /, is_doing_triumph: bool) -> Iterator[Self]:
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
