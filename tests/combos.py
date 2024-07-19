from solve.combo import Combination, Node
from solve.shapes import circle, square, triangle

_all_combinations_n = 3 * 1 * 3 * 2 * 1 * 2 * 1 * 1 * 1
_all_combinations = [
    Combination(
        left=Node.from_inner_and_other(circle, circle),
        middle=Node.from_inner_and_other(triangle, triangle),
        right=Node.from_inner_and_other(square, square),
        ),
    Combination(
        left=Node.from_inner_and_other(circle, circle),
        middle=Node.from_inner_and_other(triangle, square),
        right=Node.from_inner_and_other(square, triangle),
        ),
    Combination(
        left=Node.from_inner_and_other(circle, triangle),
        middle=Node.from_inner_and_other(triangle, circle),
        right=Node.from_inner_and_other(square, square),
        ),
    Combination(
        left=Node.from_inner_and_other(circle, triangle),
        middle=Node.from_inner_and_other(triangle, square),
        right=Node.from_inner_and_other(square, circle),
        ),
    Combination(
        left=Node.from_inner_and_other(circle, square),
        middle=Node.from_inner_and_other(triangle, circle),
        right=Node.from_inner_and_other(square, triangle),
        ),
    Combination(
        left=Node.from_inner_and_other(circle, square),
        middle=Node.from_inner_and_other(triangle, triangle),
        right=Node.from_inner_and_other(square, circle),
        ),
    Combination(
        left=Node.from_inner_and_other(circle, circle),
        middle=Node.from_inner_and_other(square, triangle),
        right=Node.from_inner_and_other(triangle, square),
        ),
    Combination(
        left=Node.from_inner_and_other(circle, circle),
        middle=Node.from_inner_and_other(square, square),
        right=Node.from_inner_and_other(triangle, triangle),
        ),
    Combination(
        left=Node.from_inner_and_other(circle, triangle),
        middle=Node.from_inner_and_other(square, circle),
        right=Node.from_inner_and_other(triangle, square),
        ),
    Combination(
        left=Node.from_inner_and_other(circle, triangle),
        middle=Node.from_inner_and_other(square, square),
        right=Node.from_inner_and_other(triangle, circle),
        ),
    Combination(
        left=Node.from_inner_and_other(circle, square),
        middle=Node.from_inner_and_other(square, circle),
        right=Node.from_inner_and_other(triangle, triangle),
        ),
    Combination(
        left=Node.from_inner_and_other(circle, square),
        middle=Node.from_inner_and_other(square, triangle),
        right=Node.from_inner_and_other(triangle, circle),
        ),
    Combination(
        left=Node.from_inner_and_other(triangle, circle),
        middle=Node.from_inner_and_other(circle, triangle),
        right=Node.from_inner_and_other(square, square),
        ),
    Combination(
        left=Node.from_inner_and_other(triangle, circle),
        middle=Node.from_inner_and_other(circle, square),
        right=Node.from_inner_and_other(square, triangle),
        ),
    Combination(
        left=Node.from_inner_and_other(triangle, triangle),
        middle=Node.from_inner_and_other(circle, circle),
        right=Node.from_inner_and_other(square, square),
        ),
    Combination(
        left=Node.from_inner_and_other(triangle, triangle),
        middle=Node.from_inner_and_other(circle, square),
        right=Node.from_inner_and_other(square, circle),
        ),
    Combination(
        left=Node.from_inner_and_other(triangle, square),
        middle=Node.from_inner_and_other(circle, circle),
        right=Node.from_inner_and_other(square, triangle),
        ),
    Combination(
        left=Node.from_inner_and_other(triangle, square),
        middle=Node.from_inner_and_other(circle, triangle),
        right=Node.from_inner_and_other(square, circle),
        ),
    Combination(
        left=Node.from_inner_and_other(triangle, circle),
        middle=Node.from_inner_and_other(square, triangle),
        right=Node.from_inner_and_other(circle, square),
        ),
    Combination(
        left=Node.from_inner_and_other(triangle, circle),
        middle=Node.from_inner_and_other(square, square),
        right=Node.from_inner_and_other(circle, triangle),
        ),
    Combination(
        left=Node.from_inner_and_other(triangle, triangle),
        middle=Node.from_inner_and_other(square, circle),
        right=Node.from_inner_and_other(circle, square),
        ),
    Combination(
        left=Node.from_inner_and_other(triangle, triangle),
        middle=Node.from_inner_and_other(square, square),
        right=Node.from_inner_and_other(circle, circle),
        ),
    Combination(
        left=Node.from_inner_and_other(triangle, square),
        middle=Node.from_inner_and_other(square, circle),
        right=Node.from_inner_and_other(circle, triangle),
        ),
    Combination(
        left=Node.from_inner_and_other(triangle, square),
        middle=Node.from_inner_and_other(square, triangle),
        right=Node.from_inner_and_other(circle, circle),
        ),
    Combination(
        left=Node.from_inner_and_other(square, circle),
        middle=Node.from_inner_and_other(circle, triangle),
        right=Node.from_inner_and_other(triangle, square),
        ),
    Combination(
        left=Node.from_inner_and_other(square, circle),
        middle=Node.from_inner_and_other(circle, square),
        right=Node.from_inner_and_other(triangle, triangle),
        ),
    Combination(
        left=Node.from_inner_and_other(square, triangle),
        middle=Node.from_inner_and_other(circle, circle),
        right=Node.from_inner_and_other(triangle, square),
        ),
    Combination(
        left=Node.from_inner_and_other(square, triangle),
        middle=Node.from_inner_and_other(circle, square),
        right=Node.from_inner_and_other(triangle, circle),
        ),
    Combination(
        left=Node.from_inner_and_other(square, square),
        middle=Node.from_inner_and_other(circle, circle),
        right=Node.from_inner_and_other(triangle, triangle),
        ),
    Combination(
        left=Node.from_inner_and_other(square, square),
        middle=Node.from_inner_and_other(circle, triangle),
        right=Node.from_inner_and_other(triangle, circle),
        ),
    Combination(
        left=Node.from_inner_and_other(square, circle),
        middle=Node.from_inner_and_other(triangle, triangle),
        right=Node.from_inner_and_other(circle, square),
        ),
    Combination(
        left=Node.from_inner_and_other(square, circle),
        middle=Node.from_inner_and_other(triangle, square),
        right=Node.from_inner_and_other(circle, triangle),
        ),
    Combination(
        left=Node.from_inner_and_other(square, triangle),
        middle=Node.from_inner_and_other(triangle, circle),
        right=Node.from_inner_and_other(circle, square),
        ),
    Combination(
        left=Node.from_inner_and_other(square, triangle),
        middle=Node.from_inner_and_other(triangle, square),
        right=Node.from_inner_and_other(circle, circle),
        ),
    Combination(
        left=Node.from_inner_and_other(square, square),
        middle=Node.from_inner_and_other(triangle, circle),
        right=Node.from_inner_and_other(circle, triangle),
        ),
    Combination(
        left=Node.from_inner_and_other(square, square),
        middle=Node.from_inner_and_other(triangle, triangle),
        right=Node.from_inner_and_other(circle, circle),
        ),
    ]

assert len(_all_combinations) == _all_combinations_n, \
    f'number of all combination must be {_all_combinations_n}'
all_combinations = {c.code: c for c in _all_combinations}
del _all_combinations, _all_combinations_n

__all__ = 'all_combinations',
