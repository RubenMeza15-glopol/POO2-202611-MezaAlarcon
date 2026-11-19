# SEMANA 14 - MODELO ESTUDIANTE

from dataclasses import dataclass


@dataclass
class Estudiante:
    codigo: int
    nombre: str
    ppa: float
    notas: list[float]