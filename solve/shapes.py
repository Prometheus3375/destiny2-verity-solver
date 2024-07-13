from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Shape:
    name: str

    def __str__(self, /) -> str:
        return self.name

    __repr__ = __str__

    def __hash__(self, /) -> int:
        return hash(self.name)


@dataclass(repr=False, eq=False, frozen=True, slots=True)
class Shape2D(Shape):
    def __add__(self, other: 'Shape2D', /) -> 'Shape3D':
        result = _addition.get((self, other))
        return NotImplemented if result is None else result

    __iadd__ = __add__


@dataclass(repr=False, eq=False, frozen=True, slots=True)
class Shape3D(Shape):
    terms: tuple[Shape2D, Shape2D]

    # noinspection PyDataclass
    def __post_init__(self, /) -> None:
        t1 = self.terms
        t2 = self.terms[1], self.terms[0]
        if t1 in _addition or t2 in _addition:
            raise ValueError(f'cannot add addition operation for {self.name}')

        _addition[t1] = _addition[t2] = self

        t3 = self, self.terms[0]
        t4 = self, self.terms[1]

        if t3 in _subtraction or t4 in _subtraction:
            raise ValueError(f'cannot add subtraction operation for {self.name}')

        _subtraction[t3] = self.terms[1]
        _subtraction[t4] = self.terms[0]

    def __sub__(self, other: Shape2D, /) -> Shape2D:
        result = _subtraction.get((self, other))
        return NotImplemented if result is None else result

    __isub__ = __sub__


_addition: dict[tuple[Shape2D, Shape2D], Shape3D] = {}
_subtraction: dict[tuple[Shape3D, Shape2D], Shape2D] = {}

circle = Shape2D('circle')
triangle = Shape2D('triangle')
square = Shape2D('square')

shape2opposite = {
    circle:   {triangle, square},
    triangle: {circle, square},
    square:   {circle, triangle},
    }

sphere = Shape3D('sphere', (circle, circle))
pyramid = Shape3D('pyramid', (triangle, triangle))
cube = Shape3D('cube', (square, square))
cone = Shape3D('cone', (circle, triangle))
cylinder = Shape3D('cylinder', (circle, square))
prism = Shape3D('prism', (triangle, square))

__all__ = (
    'Shape2D',
    'Shape3D',
    'circle',
    'triangle',
    'shape2opposite',
    'square',
    'sphere',
    'pyramid',
    'cube',
    'cone',
    'cylinder',
    'prism',
    )
