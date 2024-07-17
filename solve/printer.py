from collections.abc import Sequence

from .states import DissectMove, PassMove, PositionsType


def print_pass_moves(
        aliases: dict[PositionsType, str],
        moves: Sequence[PassMove],
        /,
        interactive: bool,
        ) -> None:
    """
    Prints pass moves to the console.
    If ``interactive`` is ``True``, prompts the user before continuing.
    """
    # Solo rooms must always be solvable in 6 passes.
    # This assertion is required for correct filling of dicts
    # initial_collect and final_collect.
    assert len(moves) == 6, f'expected 6 moves for solo rooms, got {len(moves)}'
    initial_collect = {}
    final_collect = {}
    for m in moves:
        if m.departure in initial_collect:
            final_collect[m.departure] = m.shape
        else:
            initial_collect[m.departure] = m.shape

    initial_msg = ', '.join(
        f'Player {aliases[position]} collects {shape}'
        for position, shape in initial_collect.items()
        )

    print_move = input if interactive else print
    print('--- STEPS IN SOLO ROOMS ---')
    print_move(initial_msg)
    for m in moves:
        print_move(
            f'Player {aliases[m.departure]}: '
            f'pass {m.shape} to {m.destination}'
            )
        shape = final_collect.pop(m.departure, None)
        if shape:
            print_move(f'Player {aliases[m.departure]}: collect {shape}')

    print(
        '--- SOLO ROOMS ARE DONE ---\n'
        'All player in the solo rooms must collect two shapes and wait\n'
        'Proceed with dissection\n'
        '--- LAST POSITION ---\n'
        f'{moves[-1].destination}'
        )


def print_dissect_moves(moves: Sequence[DissectMove], /, interactive: bool) -> None:
    """
    Prints dissect moves to the console.
    If ``interactive`` is ``True``, prompts the user before continuing.
    """
    print_move = input if interactive else print

    print('--- STEPS FOR DISSECTION ---')
    for m in moves:
        print_move(f'Dissect {m.shape} from {m.destination}')

    print(
        '--- DISSECTION IS DONE ---\n'
        'All players in the solo rooms must leave them\n'
        '--- LAST POSITION ---\n'
        f'{moves[-1].destination}'
        )


__all__ = 'print_pass_moves', 'print_dissect_moves'
