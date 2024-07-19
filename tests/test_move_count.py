from collections.abc import Callable
from unittest import TestCase

from solve.combo import Combination
from solve.key_sets import *
from solve.states import LEFT, MIDDLE, RIGHT, StateWithAllPositions
from . import move_count_dissection, move_count_rooms
from .combos import all_combinations


class TestMoveCount(TestCase):
    def _test_all[S, M](
            self,
            create_state: Callable[[Combination, KeySetType], StateWithAllPositions[S, M]],
            /,
            *,
            move_count_mixed: dict[str, int],
            move_count_double1: dict[str, int],
            move_count_double2: dict[str, int],
            ) -> None:
        key_sets = KSMixed, KSDouble1, KSDouble2
        key_set_names = 'KSMixed', 'KSDouble1', 'KSDouble2'
        move_numbers = move_count_mixed, move_count_double1, move_count_double2
        solve_args = (False, None), (True, LEFT), (True, MIDDLE), (True, RIGHT)
        for ks, ks_name, mapping in zip(key_sets, key_set_names, move_numbers):
            for code, combo in all_combinations.items():
                expected_move_count = mapping[code]
                state = create_state(combo, ks)
                for with_triumph, last_position in solve_args:
                    solved = state.solve(with_triumph, last_position)
                    actual_move_count = len(solved.moves_made)
                    with self.subTest(
                            ks=ks_name,
                            code=code,
                            with_triumph=with_triumph,
                            last_position=last_position,
                            ):
                        self.assertEqual(expected_move_count, actual_move_count)

    def test_rooms(self, /) -> None:
        self._test_all(
            Combination.to_room_state,
            move_count_mixed=move_count_rooms.number_of_moves_mixed,
            move_count_double1=move_count_rooms.number_of_moves_double1,
            move_count_double2=move_count_rooms.number_of_moves_double2,
            )

    def test_dissection(self, /) -> None:
        self._test_all(
            Combination.to_statue_state,
            move_count_mixed=move_count_dissection.number_of_moves_mixed,
            move_count_double1=move_count_dissection.number_of_moves_double1,
            move_count_double2=move_count_dissection.number_of_moves_double2,
            )
