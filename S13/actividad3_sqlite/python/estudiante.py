
# SEMANA 13 - ACTIVIDAD 1
# MODELO ESTUDIANTE

# Importamos dataclass para crear clases que almacenan datos.
from dataclasses import dataclass

# Definimos la clase Estudiante.
@dataclass
class Estudiante:

    # Código único del estudiante.
    codigo: int

    # Nombre completo del estudiante.
    nombre: str

    # Promedio ponderado académico.
    ppa: float

    # Lista de notas del estudiante.
    notas: list[float]
