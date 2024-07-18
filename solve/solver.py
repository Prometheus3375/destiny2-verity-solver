from .states import *


def solve_state[S, M](
        initial_state: StateWithAllPositions[S, M],
        /,
        is_doing_triumph: bool,
        last_position_touched: str | None = None,
        ) -> StateWithAllPositions[S, M]:
    """
    Makes moves starting from the given initial state until one of the next states is done.
    """
    # region First cycle
    if is_doing_triumph and last_position_touched:
        states = [
            next_state
            for next_state in initial_state.next_states(is_doing_triumph)
            if last_position_touched != next_state.first_position
            ]
    else:
        states = list(initial_state.next_states(is_doing_triumph))

    # endregion

    for _ in range(initial_state.max_cycles - 1):
        states = [
            next_state
            for state in states
            for next_state in state.next_states(is_doing_triumph)
            ]
        for state in states:
            if state.is_done:
                return state
    else:
        raise ValueError(
            f'cannot solve encounter with initial {initial_state} '
            f'within {initial_state.max_cycles} cycles'
            )


__all__ = 'solve_state',
