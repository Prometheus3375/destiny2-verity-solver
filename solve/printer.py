from collections import defaultdict, deque

from .players import AliasMappingType
from .states import StateOfAllRooms, StateOfAllStatues


def print_pass_moves(
        state: StateOfAllRooms,
        aliases: AliasMappingType,
        /,
        interactive: bool,
        ) -> None:
    """
    Prints pass moves to the console.
    If ``interactive`` is ``True``, prompts the user before continuing.
    """
    print('--- FINAL SHAPES FROM LEFT TO RIGHT ---')
    print(state.left.current_key, state.middle.current_key, state.right.current_key)

    position2collect = defaultdict(deque)
    for m in state.moves_made:
        position2collect[m.departure].appendleft(m.shape)

    initial_msg = ', '.join(
        f'Player {aliases[position]} collects {shapes.pop()}'
        for position, shapes in position2collect.items()
        )

    print_move = input if interactive else print
    print('--- STEPS IN SOLO ROOMS ---')
    print_move(initial_msg)
    for m in state.moves_made:
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
        f'{state.last_position}'
        )


def print_dissect_moves(state: StateOfAllStatues, /, interactive: bool) -> None:
    """
    Prints dissect moves to the console.
    If ``interactive`` is ``True``, prompts the user before continuing.
    """
    print('--- FINAL SHAPES FROM LEFT TO RIGHT ---')
    print(state.left.shape_held, state.middle.shape_held, state.right.shape_held)

    print_move = input if interactive else print
    print('--- STEPS FOR DISSECTION ---')
    for m in state.moves_made:
        print_move(f'Dissect {m.shape} from {m.destination}')

    print(
        '--- DISSECTION IS DONE ---\n'
        'All players in the solo rooms must leave them\n'
        '--- LAST POSITION ---\n'
        f'{state.last_position}'
        )


__all__ = 'print_pass_moves', 'print_dissect_moves'
