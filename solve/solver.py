from itertools import chain
from typing import Unpack

from .shapes import *
from .states import *

LIMIT_ROOMS = 6
LIMIT_STATUES = 3


def solve_rooms(
        is_doing_triumph: bool,
        last_position: PositionsType | None,
        **kw: Unpack[InitRoomsKwargs],
        ) -> tuple[list[PassMove], PositionsType]:
    """
    A convenience function to solve all solo rooms.
    """
    initial_state = init_rooms(**kw)
    final = solve_state(initial_state, LIMIT_ROOMS, is_doing_triumph, last_position)
    return list(final.moves_made), final.last_position


def solve_statues(
        is_doing_triumph: bool,
        last_position: PositionsType | None,
        **kw: Unpack[InitStatuesKwargs],
        ) -> tuple[list[DissectMove], PositionsType]:
    """
    A convenience function to solve all statues.
    """
    initial_state = init_statues(**kw)
    final = solve_state(initial_state, LIMIT_STATUES, is_doing_triumph, last_position)
    return list(final.moves_made), final.last_position


def solve_encounter(
        *,
        left_inner_shape: Shape2D,
        left_other_shape: Shape2D,
        middle_inner_shape: Shape2D,
        middle_other_shape: Shape2D,
        right_inner_shape: Shape2D,
        right_other_shape: Shape2D,
        left_held_shape: Shape3D,
        middle_held_shape: Shape3D,
        right_held_shape: Shape3D,
        is_doing_triumph: bool,
        last_position: PositionsType | None,
        ) -> tuple[list[PassMove], list[DissectMove], PositionsType]:
    """
    Initializes Verity encounter, solves it and returns necessary moves.
    """
    pass_moves, last_position = solve_rooms(
        left_inner_shape=left_inner_shape,
        left_other_shape=left_other_shape,
        middle_inner_shape=middle_inner_shape,
        middle_other_shape=middle_other_shape,
        right_inner_shape=right_inner_shape,
        right_other_shape=right_other_shape,
        is_doing_triumph=is_doing_triumph,
        last_position=last_position,
        )

    dissect_moves, last_position = solve_statues(
        left_inner_shape=left_inner_shape,
        left_held_shape=left_held_shape,
        middle_inner_shape=middle_inner_shape,
        middle_held_shape=middle_held_shape,
        right_inner_shape=right_inner_shape,
        right_held_shape=right_held_shape,
        is_doing_triumph=is_doing_triumph,
        last_position=last_position,
        )

    return pass_moves, dissect_moves, last_position


def solve_state[S, M](
        initial_state: StateWithAllPositions[S, M],
        move_limit: int,
        /,
        is_doing_triumph: bool,
        last_position_touched: str | None = None,
        ) -> StateWithAllPositions[S, M]:
    """
    Makes moves from initial state until one of the next state will be completed.
    The number of moves are limited by argument ``move_limit``.
    """
    states = [initial_state]
    for _ in range(move_limit):
        states = list(chain.from_iterable(s.make_all_moves(is_doing_triumph) for s in states))
        for s in states:
            if s.is_done and (not is_doing_triumph or last_position_touched != s.first_position):
                return s
    else:
        raise ValueError(
            f'cannot solve encounter with initial {initial_state} '
            f'within {move_limit} moves'
            )
