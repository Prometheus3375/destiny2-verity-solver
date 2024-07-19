from collections.abc import Mapping
from dataclasses import dataclass

from .shapes import Shape2D
from .states import PositionsType

type AliasMappingType = Mapping[PositionsType, str]


@dataclass(frozen=True, kw_only=True, slots=True)
class Player:
    alias: str
    their_shape: Shape2D
    other_shape: Shape2D


__all__ = 'Player', 'AliasMappingType'
