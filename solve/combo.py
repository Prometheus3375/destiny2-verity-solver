from dataclasses import dataclass
from typing import Self

from .key_sets import *
from .shapes import Shape2D
from .states import StateOfAllRooms, StateOfAllStatues, init_rooms, init_statues


@dataclass(frozen=True, slots=True)
class Node:
    inner: Shape2D
    available: tuple[Shape2D, Shape2D]

    @property
    def code(self, /) -> str:
        """
        Numeric code for this node.
        """
        return f'{self.inner.code}[{self.available[0].code}{self.available[1].code}]'

    @classmethod
    def from_inner_and_other(cls, inner: Shape2D, other: Shape2D, /) -> Self:
        """
        Creates a new node using inner shape and other shape.
        Both inner shape and other shape are added as available.
        """
        return cls(inner, (inner, other))


@dataclass(frozen=True, kw_only=True, slots=True)
class Combination:
    left: Node
    middle: Node
    right: Node

    @property
    def code(self, /) -> str:
        """
        Numeric code for this combination.
        """
        return f'{self.left.code}-{self.middle.code}-{self.right.code}'

    def to_room_state(self, key_set: KeySetType, /) -> StateOfAllRooms:
        return init_rooms(
            left_inner_shape=self.left.inner,
            left_other_shape=self.left.available[1],
            middle_inner_shape=self.middle.inner,
            middle_other_shape=self.middle.available[1],
            right_inner_shape=self.right.inner,
            right_other_shape=self.right.available[1],
            key_set=key_set,
            )

    def to_statue_state(self, key_set: KeySetType, /) -> StateOfAllStatues:
        return init_statues(
            left_inner_shape=self.left.inner,
            left_held_shape=self.left.available[0] + self.left.available[1],
            middle_inner_shape=self.middle.inner,
            middle_held_shape=self.middle.available[0] + self.middle.available[1],
            right_inner_shape=self.right.inner,
            right_held_shape=self.right.available[0] + self.right.available[1],
            key_set=key_set,
            )


code_to_best_ks = {
    '0[03]-3[34]-4[40]': KSDouble2,
    '0[04]-3[30]-4[43]': KSDouble1,
    '0[03]-4[40]-3[34]': KSDouble2,
    '0[04]-4[43]-3[30]': KSDouble1,
    '3[30]-0[04]-4[43]': KSDouble1,
    '3[34]-0[03]-4[40]': KSDouble2,
    '3[30]-4[43]-0[04]': KSDouble1,
    '3[34]-4[40]-0[03]': KSDouble2,
    '4[40]-0[03]-3[34]': KSDouble2,
    '4[43]-0[04]-3[30]': KSDouble1,
    '4[40]-3[34]-0[03]': KSDouble2,
    '4[43]-3[30]-0[04]': KSDouble1,
    }


def get_best_double_key(*, rooms: Combination | None, statues: Combination | None) -> KeySetType:
    """
    Determines the best double key set for provided combinations.

    At first evaluates the best key set for room combination.
    If there is no best key or the combination is not provided,
    then it uses statue combination for evaluation.
    If either evaluation is indifferent, returns ``KSDouble1``.
    """
    if rooms is not None:
        best_ks = code_to_best_ks.get(rooms.code)
        if best_ks is not None:
            return best_ks

    if statues is not None:
        best_ks = code_to_best_ks.get(statues.code)
        if best_ks is not None:
            return best_ks

    return KSDouble1


__all__ = 'Node', 'Combination', 'get_best_double_key'
