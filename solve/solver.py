from itertools import chain

from .states import *

LIMIT_ROOMS = 6
LIMIT_STATUES = 3


def solve_rooms(
        initial_state: StateOfAllRooms,
        /,
        is_doing_triumph: bool,
        last_position_touched: PositionsType | None,
        ) -> list[PassMove]:
    """
    A convenience function to solve all solo rooms.
    """
    final = solve_state(initial_state, LIMIT_ROOMS, is_doing_triumph, last_position_touched)
    return list(final.moves_made)


def solve_statues(
        initial_state: StateOfAllStatues,
        /,
        is_doing_triumph: bool,
        last_position_touched: PositionsType | None,
        ) -> list[DissectMove]:
    """
    A convenience function to solve all statues.
    """
    final = solve_state(initial_state, LIMIT_STATUES, is_doing_triumph, last_position_touched)
    return list(final.moves_made)


def solve_state[S, M](
        initial_state: StateWithAllPositions[S, M],
        move_limit: int,
        /,
        is_doing_triumph: bool,
        last_position_touched: str | None = None,
        ) -> StateWithAllPositions[S, M]:
    """
    Makes moves from initial state until one of the next state is completed.
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


__all__ = 'solve_rooms', 'solve_statues', 'solve_state'
