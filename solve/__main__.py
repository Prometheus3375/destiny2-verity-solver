from argparse import ArgumentParser, RawTextHelpFormatter
from enum import StrEnum
from typing import assert_never

import solve
from .config import read_config
from .printer import *
from .solver import solve_rooms, solve_statues


class EncounterParts(StrEnum):
    SOLO_ROOMS = 'solo-rooms'
    DISSECTION = 'dissection'
    BOTH = 'both'


def main(
        config_filepath: str,
        encounter_part: EncounterParts,
        /,
        interactive: bool,
        ) -> None:
    config = read_config(config_filepath)

    match encounter_part:
        case EncounterParts.SOLO_ROOMS:
            do_rooms = True
            do_dissect = False
        case EncounterParts.DISSECTION:
            do_rooms = False
            do_dissect = True
        case EncounterParts.BOTH:
            do_rooms = True
            do_dissect = True
        case unknown:
            assert_never(unknown)

    with_triumph = config.is_doing_triumph
    last_position = config.last_position
    if do_rooms:
        room_state, aliases = config.init_rooms()
        moves = solve_rooms(room_state, with_triumph, last_position)
        print_pass_moves(aliases, moves, interactive)
        last_position = moves[-1].destination

    if do_dissect:
        if do_rooms: print('\n')

        statue_state = config.init_statues()
        moves = solve_statues(statue_state, with_triumph, last_position)
        print_dissect_moves(moves, interactive)


def define_parser() -> ArgumentParser:
    parser = ArgumentParser(
        prog=f'python -m {solve.__name__}',
        description='A script for solving 4th encounter of Salvation Edge in Destiny 2',
        formatter_class=RawTextHelpFormatter,
        add_help=False,
        )

    parser.add_argument(
        'encounter_part',
        metavar='ENCOUNTER-PART',
        choices=EncounterParts,
        default=EncounterParts.BOTH,
        help='Specifies what encounter part to solve.\n'
             '  - "solo-rooms" - the script prints solution only for solo rooms.\n'
             '  - "dissection" - the script prints solution only for dissection.\n'
             '  - "both" - the script prints solution for solo rooms, then for dissection.\n'
             'Defaults to "both".',
        )

    parser.add_argument(
        '-h',
        '--help',
        action='help',
        help='If specified, the script shows this help message and exits.',
        )

    parser.add_argument(
        '-i',
        '--interactive',
        action='store_true',
        help='If specified, the script requests user prompt after every step of the solution. '
             'The user must press Enter to go to the next step.',
        )

    parser.add_argument(
        '-c',
        '--config',
        default='config.toml',
        help='Path to the configuration file with the encounter settings. '
             'You can create one from file "config-template.toml". '
             'Defaults to "config.toml".',
        )

    return parser


if __name__ == '__main__':
    args = define_parser().parse_args()
    main(args.config, args.encounter_part, args.interactive)
