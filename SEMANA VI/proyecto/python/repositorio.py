# ── repositorio.py — Repositorio genérico con TypeVar (Python) ──────────
from functools import reduce
from typing import Callable, Generic, Iterator, TypeVar

# TypeVar: variable de tipo que mypy usará para verificación estática
T = TypeVar("T")    # tipo de la entidad
ID = TypeVar("ID")  # tipo del identificador
U = TypeVar("U")    # tipo del acumulador


class Repositorio(Generic[T, ID]):
    """
    Repositorio genérico — funciona para cualquier (Entidad, TipoID).

    Uso:
        repo = Repositorio[Estudiante, int](lambda e: e.codigo)
        repo = Repositorio[Curso, str](lambda c: c.codigo)
    """

    def __init__(self, fn_id: Callable[[T], ID]):
        """fn_id: función que extrae el ID de una entidad."""
        self._fn_id: Callable[[T], ID] = fn_id
        self._datos: dict[ID, T] = {}

    # ── CRUD ─────────────────────────────────────────────────────────────
    def guardar(self, entidad: T) -> None:
        """Guarda o sobreescribe la entidad con su ID."""
        self._datos[self._fn_id(entidad)] = entidad

    def buscar(self, id_: ID) -> T | None:
        """Retorna la entidad o None si no existe."""
        return self._datos.get(id_)

    def eliminar(self, id_: ID) -> bool:
        """Retorna True si existía y fue eliminada."""
        if id_ in self._datos:
            del self._datos[id_]
            return True
        return False

    def existe(self, id_: ID) -> bool:
        return id_ in self._datos

    # ── CONSULTAS ─────────────────────────────────────────────────────────
    def todos(self) -> list[T]:
        """Lista de todas las entidades (copia)."""
        return list(self._datos.values())

    def filtrar(self, pred: Callable[[T], bool]) -> list[T]:
        """Retorna las entidades que satisfacen el predicado."""
        return [e for e in self._datos.values() if pred(e)]

    def ordenar(self, key: Callable[[T], object], reverse: bool = False) -> list[T]:
        """Retorna las entidades ordenadas por key."""
        return sorted(self._datos.values(), key=key, reverse=reverse)  # type: ignore[arg-type]

    def acumular(self, inicial: U, f: Callable[[U, T], U]) -> U:
        """Reduce todas las entidades con una función acumuladora."""
        return reduce(f, self._datos.values(), inicial)

    def contar(self, pred: Callable[[T], bool]) -> int:
        """Cuenta elementos que satisfacen el predicado."""
        return sum(1 for e in self._datos.values() if pred(e))

    def primero(self, pred: Callable[[T], bool]) -> T | None:
        """Retorna el primer elemento que satisface pred, o None."""
        return next((e for e in self._datos.values() if pred(e)), None)

    # ── PROTOCOLO PYTHON ─────────────────────────────────────────────────
    def __len__(self) -> int: return len(self._datos)
    def __contains__(self, id_: object) -> bool: return id_ in self._datos
    def __iter__(self) -> Iterator[T]: return iter(self._datos.values())

    def estadisticas(self, attr: str) -> dict[str, float | int | None]:
        """Calcula min, max y promedio de un atributo numérico."""
        valores = [getattr(e, attr) for e in self._datos.values()]
        if not valores:
            return {"min": None, "max": None, "promedio": None, "n": 0}
        return {
            "min": min(valores),
            "max": max(valores),
            "promedio": sum(valores) / len(valores),
            "n": len(valores),
        }
