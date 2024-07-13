import tomllib
from collections.abc import Sequence
from dataclasses import dataclass

from .players import Player
from .shapes import *
from .states import LEFT, MIDDLE, PositionsType, RIGHT, is_position

number2shape = {
    0:  circle,
    3:  triangle,
    4:  square,

    20: sphere,
    23: pyramid,
    33: pyramid,
    24: cube,
    44: cube,

    30: cone,
    40: cylinder,
    34: prism,
    43: prism,
    }


@dataclass(frozen=True, kw_only=True, slots=True)
class Config:
    inner_shapes: Sequence[Shape2D]
    held_shapes: Sequence[Shape3D]
    players: Sequence[Player]
    is_doing_triumph: bool
    last_position: PositionsType | None


def read_config(filepath: str, /) -> Config:
    """
    Reads configuration file from provided filepath
    and returns an instance of :class:`Config`.
    """
    with open(filepath, 'rb') as f:
        data = tomllib.load(f)

    is_doing_triumph = data.get('is_doing_triumph', False)
    assert isinstance(is_doing_triumph, bool), 'is_doing_triumph must be a boolean'

    last_position = data.get('last_position', '')
    if last_position == '':
        last_position = None

    assert last_position is None or is_position(last_position), \
        f'last_position must be \'\', {LEFT!r}, {MIDDLE!r} or {RIGHT!r}'

    inner_shapes = data['inner_shapes']
    assert isinstance(inner_shapes, list) and len(inner_shapes) == 3, \
        f'inner_shapes must be a permutation of [0, 3, 4]'

    held_shapes = data['held_shapes']
    assert isinstance(held_shapes, list) and len(held_shapes) == 3, \
        f'held_shapes must be a list of three numbers representing 3D shapes'

    inner: list[Shape2D] = [number2shape[i] for i in inner_shapes]
    held: list[Shape3D] = [number2shape[i] for i in held_shapes]

    player1_kw = data['player1']
    player2_kw = data['player2']
    player3_kw = data['player3']
    players = []
    for i, p in enumerate((player1_kw, player2_kw, player3_kw), 1):
        cond = isinstance(p, dict) and p.keys() == Player.__annotations__.keys()
        assert cond, (
            f'player{i} must be a mapping '
            f'and have values for fields {', '.join(Player.__annotations__)}'
        )
        p['their_shape'] = number2shape[p['their_shape']]
        p['other_shape'] = number2shape[p['other_shape']]
        players.append(Player(**p))

    return Config(
        inner_shapes=inner,
        held_shapes=held,
        players=players,
        is_doing_triumph=is_doing_triumph,
        last_position=last_position,
        )


__all__ = 'Config', 'read_config'
