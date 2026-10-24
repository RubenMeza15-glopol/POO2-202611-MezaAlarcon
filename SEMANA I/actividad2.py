# SU SOLUCIÓN REFACTORIZADA — Práctica S1, Actividad 2

from dataclasses import dataclass
from typing import Optional


@dataclass
class Nota:
    curso: str
    calificacion: float


class Estudiante:
    def __init__(self, nombre: str, codigo: int, escuela: str):
        self._nombre = nombre
        self._codigo = codigo
        self._escuela = escuela
        self._notas = []

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def codigo(self) -> int:
        return self._codigo

    def agregar_nota(
        self,
        curso: str,
        calificacion: float
    ) -> None:

        if not 0 <= calificacion <= 20:
            raise ValueError(
                "La calificación debe estar entre 0 y 20"
            )

        self._notas.append(
            Nota(curso, calificacion)
        )

    def calcular_ppa(self) -> float:
        if not self._notas:
            return 0.0

        total = sum(
            nota.calificacion
            for nota in self._notas
        )

        return total / len(self._notas)

    def __str__(self) -> str:
        return (
            f"[{self._codigo}] "
            f"{self._nombre} "
            f"({self._escuela})"
        )


# Prueba — debe ejecutar sin errores

e = Estudiante(
    "Juan Carlos Mamani Quispe",
    20210500,
    "Ing. Sistemas"
)

e.agregar_nota("POO II", 16)
e.agregar_nota("Base de Datos I", 14)

print(e)

print(f"PPA: {e.calcular_ppa():.2f}")

try:
    e.agregar_nota("Redes", 25)
except ValueError as ex:
    print(
        f"\nError capturado correctamente: {ex}"
    )