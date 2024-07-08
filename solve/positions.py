from collections.abc import Iterator
from inspect import signature
from typing import Protocol, Self

LEFT = 'left'
MIDDLE = 'middle'
RIGHT = 'right'
POSITIONS = dict.fromkeys((LEFT, MIDDLE, RIGHT))
POSITIONS_MSG = f'{LEFT!r}, {MIDDLE!r} or {RIGHT!r}'


class State(Protocol):
    @property
    def is_done(self, /) -> bool:
        """Whether this state is done."""


class StateWithPositions[S: State, M]:
    """
    Base class for holding states of positions and moves made.
    """
    __slots__ = 'left', 'middle', 'right', 'moves_made'

    def __init__(self, /, left: S, middle: S, right: S, moves_made: tuple[M, ...] = ()) -> None:
        self.left = left
        self.middle = middle
        self.right = right
        self.moves_made = moves_made

    # region Verify that constructor has POSITIONS as keyword arguments
    signature_ = signature(__init__)
    kwargs = {
        p.name
        for p in signature_.parameters.values()
        if p.kind is p.KEYWORD_ONLY or p.kind is p.POSITIONAL_OR_KEYWORD
        }

    assert kwargs >= POSITIONS.keys(), f'Encounter state must have position attributes'
    del signature_, kwargs
    # endregion

    @property
    def is_done(self, /) -> bool:
        """
        Whether states in all positions are done.
        """
        return self.left.is_done and self.middle.is_done and self.right.is_done

    @property
    def first_position(self, /) -> str:
        """
        First position touched via moves made.
        """
        raise NotImplementedError

    @property
    def last_position(self, /) -> str:
        """
        Last position touched via moves made.
        """
        raise NotImplementedError

    def make_all_moves(self, /, is_doing_triumph: bool) -> Iterator[Self]:
        """
        Yields all possible next states.
        """
        raise NotImplementedError

    def __repr__(self, /) -> str:
        return (
            f'{self.__class__.__name__}('
            f'{self.left!r}, '
            f'{self.middle!r}, '
            f'{self.right!r}, '
            f'{self.moves_made}'
            f')'
        )


__all__ = 'LEFT', 'MIDDLE', 'RIGHT', 'POSITIONS', 'POSITIONS_MSG', 'StateWithPositions'
