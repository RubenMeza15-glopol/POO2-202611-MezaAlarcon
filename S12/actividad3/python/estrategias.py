
# ACTIVIDAD 3 - MVC CON OBSERVER
# PATRON STRATEGY: estrategias de calculo del promedio.

from typing import Protocol

# Contrato común para todas las estrategias.
class EstrategiaPromedio(Protocol):
    def calcular(self, notas: list[float]) -> float:
        ...

# Estrategia 1: calcula el promedio simple.
class PromedioSimple:
    def calcular(self, notas: list[float]) -> float:
        if not notas:
            return 0.0

        return sum(notas) / len(notas)

# Estrategia 2: calcula el promedio moderado.
class PromedioModerado:
    def calcular(self, notas: list[float]) -> float:
        if not notas:
            return 0.0

        # Ordena las notas de menor a mayor.
        notas_ordenadas = sorted(notas)

        # Si hay tres o más notas, elimina la menor.
        if len(notas_ordenadas) >= 3:
            notas_ordenadas = notas_ordenadas[1:]

        # Calcula el promedio de las notas restantes.
        return sum(notas_ordenadas) / len(notas_ordenadas)
