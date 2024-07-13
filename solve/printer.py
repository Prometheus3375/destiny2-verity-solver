from .states import DissectMove, PassMove, PositionsType


def print_pass_moves(
        aliases: dict[PositionsType, str],
        moves: list[PassMove],
        /,
        interactive: bool,
        ) -> None:
    """
    Prints pass moves to the console.
    If ``interactive`` is ``True``, prompts the user before continuing.
    """
    print_move = input if interactive else print
    for m in moves:
        print_move(
            f'Player {aliases[m.departure]} ({m.departure}): '
            f'pass {m.shape} to {m.destination}'
            )

    print(
        '--- SOLO ROOMS ARE DONE ---\n'
        'All player in the solo rooms must collect two shapes and wait\n'
        'Proceed with dissection\n\n'
        '--- LAST POSITION ---\n'
        f'{moves[-1].destination}'
        )


def print_dissect_moves(moves: list[DissectMove], /, interactive: bool) -> None:
    """
    Prints dissect moves to the console.
    If ``interactive`` is ``True``, prompts the user before continuing.
    """
    print_move = input if interactive else print
    for m in moves:
        print_move(f'Dissect {m.shape} from {m.destination}')

    print(
        '--- DISSECTION IS DONE ---\n'
        'All players in the solo rooms must leave them\n\n'
        '--- LAST POSITION ---\n'
        f'{moves[-1].destination}'
        )


__all__ = 'print_pass_moves', 'print_dissect_moves'
