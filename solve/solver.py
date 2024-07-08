from itertools import chain

from .positions import StateWithPositions
from .rooms import PassMove, init_rooms
from .shapes import *
from .statues import DissectMove, init_statues

LIMIT_ROOMS = 6
LIMIT_STATUES = 3


def solve_encounter(
        *,
        left_alias: str,
        middle_alias: str,
        right_alias: str,
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
        ) -> tuple[list[PassMove], list[DissectMove]]:
    """
    Initializes Verity encounter, solves it and returns necessary moves.
    """
    initial_room_state = init_rooms(
        left_alias=left_alias,
        left_shape=left_inner_shape,
        left_other_shape=left_other_shape,
        middle_alias=middle_alias,
        middle_shape=middle_inner_shape,
        middle_other_shape=middle_other_shape,
        right_alias=right_alias,
        right_shape=right_inner_shape,
        right_other_shape=right_other_shape,
        )

    initial_statue_state = init_statues(
        left_alias=left_alias,
        left_inner_shape=left_inner_shape,
        left_held_shape=left_held_shape,
        middle_alias=middle_alias,
        middle_inner_shape=middle_inner_shape,
        middle_held_shape=middle_held_shape,
        right_alias=right_alias,
        right_inner_shape=right_inner_shape,
        right_held_shape=right_held_shape,
        )

    room_moves, lp = solve_state(initial_room_state, LIMIT_ROOMS, is_doing_triumph)
    statue_moves, _ = solve_state(initial_statue_state, LIMIT_STATUES, is_doing_triumph, lp)
    return room_moves, statue_moves


def solve_state[S, M](
        initial_state: StateWithPositions[S, M],
        move_limit: int,
        /,
        is_doing_triumph: bool,
        last_position_touched: str | None = None,
        ) -> tuple[list[M], str]:
    """
    Makes moves from initial state until one of the next state will be completed.
    The number of moves are limited by argument ``move_limit``.
    """
    states = [initial_state]
    for _ in range(move_limit):
        states = list(chain.from_iterable(s.make_all_moves(is_doing_triumph) for s in states))
        for s in states:
            if s.is_done and (not is_doing_triumph or last_position_touched != s.first_position):
                return list(s.moves_made), s.last_position
    else:
        raise ValueError(
            f'cannot solve encounter with initial {initial_state} '
            f'within {move_limit} moves'
            )
