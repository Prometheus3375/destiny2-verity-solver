from collections import defaultdict, deque
from collections.abc import Sequence

from .players import AliasMappingType
from .states import DissectMove, PassMove


def print_pass_moves(
        aliases: AliasMappingType,
        moves: Sequence[PassMove],
        /,
        interactive: bool,
        ) -> None:
    """
    Prints pass moves to the console.
    If ``interactive`` is ``True``, prompts the user before continuing.
    """
    position2collect = defaultdict(deque)
    for m in moves:
        position2collect[m.departure].appendleft(m.shape)

    initial_msg = ', '.join(
        f'Player {aliases[position]} collects {shapes.pop()}'
        for position, shapes in position2collect.items()
        )

    print_move = input if interactive else print
    print('--- STEPS IN SOLO ROOMS ---')
    print_move(initial_msg)
    for m in moves:
        print_move(
            f'Player {aliases[m.departure]}: '
            f'pass {m.shape} to {m.destination}'
            )
        shapes = position2collect[m.departure]
        if shapes:
            print_move(f'Player {aliases[m.departure]}: collect {shapes.pop()}')

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
