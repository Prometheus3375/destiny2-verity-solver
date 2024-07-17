from itertools import chain

from .states import *


def solve_state[S, M](
        initial_state: StateWithAllPositions[S, M],
        /,
        is_doing_triumph: bool,
        last_position_touched: str | None = None,
        ) -> StateWithAllPositions[S, M]:
    """
    Makes moves stating from the given initial state until one of the states is completed.
    """
    max_cycles = initial_state.max_cycles
    states = [initial_state]
    for _ in range(max_cycles):
        states = list(chain.from_iterable(s.next_states(is_doing_triumph) for s in states))
        for s in states:
            if s.is_done and (not is_doing_triumph or last_position_touched != s.first_position):
                return s
    else:
        raise ValueError(
            f'cannot solve encounter with initial {initial_state} '
            f'within {max_cycles} cycles'
            )


__all__ = 'solve_state',
