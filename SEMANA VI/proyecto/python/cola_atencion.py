# ── cola_atencion.py — cola FIFO con deque: append/popleft O(1) ─────────
from collections import deque
from typing import Generic, Iterator, TypeVar

T = TypeVar("T")


class ColaAtencion(Generic[T]):
    def __init__(self) -> None:
        self._cola: deque[T] = deque()

    def encolar(self, elemento: T) -> None:
        self._cola.append(elemento)  # O(1)

    def atender(self) -> T | None:
        return self._cola.popleft() if self._cola else None  # O(1)

    def __len__(self) -> int: return len(self._cola)
    def __iter__(self) -> Iterator[T]: return iter(self._cola)
    def __bool__(self) -> bool: return bool(self._cola)
