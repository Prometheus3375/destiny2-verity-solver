from collections.abc import Sequence
from dataclasses import dataclass

from solve.shapes import Shape2D
from solve.states import LEFT, MIDDLE, PositionsType, RIGHT, StateOfAllRooms, init_rooms


@dataclass(frozen=True, kw_only=True, slots=True)
class Player:
    alias: str
    their_shape: Shape2D
    other_shape: Shape2D


def init_rooms_from_players(
        players: Sequence[Player],
        inner_shapes: Sequence[Shape2D],
        /,
        ) -> tuple[StateOfAllRooms, dict[PositionsType, str]]:
    """
    Takes three players in solo rooms and 2D shapes of statues there in order from left to right.
    Returns initial state of solo rooms a mapping of positions to player aliases.
    """
    assert len(players) == len(inner_shapes) == 3, f'number of players and shapes must be 3'
    inner2person = {
        i: p
        for i in inner_shapes
        for p in players
        if p.their_shape == i
        }
    aliases = dict(zip((LEFT, MIDDLE, RIGHT), (inner2person[i].alias for i in inner_shapes)))
    other = tuple(inner2person[i].other_shape for i in inner_shapes)
    state = init_rooms(
        left_inner_shape=inner_shapes[0],
        left_other_shape=other[0],
        middle_inner_shape=inner_shapes[1],
        middle_other_shape=other[1],
        right_inner_shape=inner_shapes[2],
        right_other_shape=other[2],
        )

    return state, aliases


__all__ = 'Player', 'init_rooms_from_players'
