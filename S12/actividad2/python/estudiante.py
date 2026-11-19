
# ACTIVIDAD 1: OBSERVER EN PYTHON 3.12
# Define los datos de un estudiante.

from dataclasses import dataclass


@dataclass
class Estudiante:
    # Código único del estudiante.
    codigo: int

    # Nombre completo.
    nombre: str

    # Promedio ponderado acumulado.
    ppa: float

    # Ciclo académico.
    ciclo: int

    # Devuelve los datos del estudiante como texto.
    def __str__(self):
        return (
            f"[{self.codigo}] {self.nombre} "
            f"- PPA: {self.ppa:.6f}"
        )
