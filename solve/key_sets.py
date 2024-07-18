from collections.abc import Mapping

from .shapes import *

type KeySetType = Mapping[Shape2D, Shape3D]

KSMixed: KeySetType = {
    circle:   prism,
    triangle: cylinder,
    square:   cone,
    }
KSDouble1: KeySetType = {
    circle:   cube,
    triangle: sphere,
    square:   pyramid,
    }
KSDouble2: KeySetType = {
    circle:   pyramid,
    triangle: cube,
    square:   sphere,
    }

__all__ = 'KeySetType', 'KSMixed', 'KSDouble1', 'KSDouble2'
