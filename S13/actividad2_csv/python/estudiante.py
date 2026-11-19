
# SEMANA 13 - ACTIVIDAD 2
# MODELO ESTUDIANTE

from dataclasses import dataclass

@dataclass
class Estudiante:
    # Código único del estudiante.
    codigo: int

    # Nombre completo.
    nombre: str

    # Promedio ponderado académico.
    ppa: float

    # Lista de notas.
    notas: list[float]
