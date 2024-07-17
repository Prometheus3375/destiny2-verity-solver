from collections import Counter
from collections.abc import Iterable, Iterator, Set
from itertools import product
from typing import Self


@Set.register
class Multiset[T]:
    """
    A special set which can hold the same object multiple times.
    """
    __slots__ = '_counter',

    def __init__(self, it: Iterable[T] | None = None, /) -> None:
        """
        :param it: An iterable of elements to initialize this set.
        """
        if isinstance(it, self.__class__):
            self._counter = it._counter.copy()
        else:
            self._counter = Counter(it)

    def __contains__(self, item: T, /) -> bool:
        return self._counter.__contains__(item)

    def __iter__(self, /) -> Iterator[T]:
        return self._counter.__iter__()

    def elements(self, /) -> Iterator[T]:
        """
        Returns an iterator of elements.
        Each element is yielded as many times as it is present in this set.
        """
        return self._counter.elements()

    def __len__(self, /) -> int:
        return self._counter.__len__()

    def total(self, /) -> int:
        """
        Returns the total number of elements in this multiset.
        """
        return self._counter.total()

    def __hash__(self, /) -> int:
        return hash(frozenset(self._counter))

    def copy(self, /) -> Self:
        """
        Makes a shallow copy of this set.
        """
        return self.__class__(self._counter)

    def add_copy(self, item: T, /) -> Self:
        """
        Copies this set and adds the given element to the copy.
        Returns the copy.
        """
        new = self.copy()
        new._counter[item] += 1
        return new

    def discard_copy(self, item: T, /) -> Self:
        """
        Copies this set and discards the given element from the copy.
        Returns the copy.
        """
        new = self.copy()
        match new._counter[item]:
            case 0: pass
            case 1: dict.__delitem__(new._counter, item)
            case count: new._counter[item] = count - 1

        return new

    def remove_copy(self, item: T, /) -> Self:
        """
        Copies this set and removes the given element from the copy.
        Returns the copy.
        Raises :class:`KeyError` if the element is not present in this set.
        """
        if item in self:
            return self.discard_copy(item)

        raise KeyError(item)

    # region Set operations.
    # For cases with generic sets use other first,
    # because they can already have necessary implementation.

    def isdisjoint(self, other: Set, /) -> bool:
        """
        Returns ``True`` if this set and other have no common elements.
        """
        for _ in product(self, other):
            return False

        return True

    def __eq__(self, other: Set[T], /) -> bool:
        if isinstance(other, self.__class__):
            return self._counter == other._counter

        if isinstance(other, Set):
            return other == self._counter.keys()

        return NotImplemented

    def __ne__(self, other: Set[T], /) -> bool:
        if isinstance(other, self.__class__):
            return self._counter != other._counter

        if isinstance(other, Set):
            return other != self._counter.keys()

        return NotImplemented

    def __lt__(self, other: Set[T], /) -> bool:
        if isinstance(other, self.__class__):
            return self._counter < other._counter

        if isinstance(other, Set):
            return other > self._counter.keys()

        return NotImplemented

    def __le__(self, other: Set[T], /) -> bool:
        if isinstance(other, self.__class__):
            return self._counter <= other._counter

        if isinstance(other, Set):
            return other >= self._counter.keys()

        return NotImplemented

    def __gt__(self, other: Set[T], /) -> bool:
        if isinstance(other, self.__class__):
            return self._counter > other._counter

        if isinstance(other, Set):
            return other < self._counter.keys()

        return NotImplemented

    def __ge__(self, other: Set[T], /) -> bool:
        if isinstance(other, self.__class__):
            return self._counter >= other._counter

        if isinstance(other, Set):
            return other <= self._counter.keys()

        return NotImplemented

    def __add__(self, other: Set[T], /) -> Self:
        if isinstance(other, self.__class__):
            new = self.copy()
            new._counter += other._counter
            return new

        if isinstance(other, Set):
            new = self.copy()
            new._counter.update(other)
            return new

        return NotImplemented

    __radd__ = __add__

    def __sub__(self, other: Set[T], /) -> Self:
        if isinstance(other, self.__class__):
            new = self.copy()
            new._counter -= other._counter
            return new

        if isinstance(other, Set):
            # From this multiset subtract other set, keeping only positive values
            new = self.copy()
            for e in other:
                match new._counter[e]:
                    case 0: pass
                    case 1: dict.__delitem__(new._counter, e)
                    case count: new._counter[e] = count - 1

            return new

        return NotImplemented

    def __rsub__(self, other: Set[T], /) -> Self:
        if isinstance(other, self.__class__):
            # From other multiset subtract this multiset.
            new = other.copy()
            new._counter -= self._counter
            return new

        if isinstance(other, Set):
            # From other set subtract this multiset, i.e.,
            # keep elements from other that are not present in this.
            # All new counts must be 1.
            return self.__class__(e for e in other if e not in self._counter)

        return NotImplemented

    def __and__(self, other: Set[T], /) -> Self:
        if isinstance(other, self.__class__):
            new = self.copy()
            new._counter &= other._counter
            return new

        if isinstance(other, Set):
            # Intersection between this multiset and other regular set, i.e.,
            # keep elements from other that are present in this.
            # All new counts must be 1.
            return self.__class__(e for e in other if e in self._counter)

        return NotImplemented

    __rand__ = __and__

    def __or__(self, other: Set[T], /) -> Self:
        if isinstance(other, self.__class__):
            new = self.copy()
            new._counter |= other._counter
            return new

        if isinstance(other, Set):
            # Union between this multiset and other regular set, i.e.,
            # keep elements from this with the same count
            # and add elements from other with count 1.
            new = self.copy()
            for e in other:
                if e not in self._counter:
                    new._counter[e] = 1

            return new

        return NotImplemented

    __ror__ = __or__

    def __xor__(self, other: Set[T], /) -> Self:
        # Regular set is a multiset with all counts being 1.
        # A symmetric difference is a difference between union and intersection.
        # Union - maximum number of counts from both multisets.
        # Intersection - minimum number of counts from both multisets.
        if isinstance(other, self.__class__):
            new = self.__class__()
            counter = new._counter
            for e in self._counter.keys() | other._counter.keys():
                counts = self._counter[e], other._counter[e]
                count = max(counts) - min(counts)
                if count > 0:
                    counter[e] = count

            return new

        if isinstance(other, Set):
            new = self.__class__()
            counter = new._counter
            for e in self._counter.keys() | other:
                counts = self._counter[e], 1 if e in other else 0
                count = max(counts) - min(counts)
                if count > 0:
                    counter[e] = count

            return new

        return NotImplemented

    __rxor__ = __xor__

    # endregion


__all__ = 'Multiset',
