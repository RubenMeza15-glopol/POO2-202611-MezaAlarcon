# ── result.py — patrón Result con Generic[T] en Python ──────────────────
from dataclasses import dataclass
from typing import Callable, Generic, TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class Result(Generic[T]):
    _valor: T | None = None
    _error: str | None = None

    @staticmethod
    def ok(valor: T) -> "Result[T]": return Result(_valor=valor)

    @staticmethod
    def fallo(e: str) -> "Result[T]": return Result(_error=e)

    @property
    def es_exito(self) -> bool: return self._error is None

    @property
    def valor(self) -> T:
        if not self.es_exito:
            raise RuntimeError(f"Result fallido: {self._error}")
        return self._valor

    @property
    def error(self) -> str:
        return self._error or ""

    def map(self, f: Callable[[T], "Result"]) -> "Result":
        """Encadenar: aplica f solo si el resultado es exitoso."""
        return f(self._valor) if self.es_exito else self
