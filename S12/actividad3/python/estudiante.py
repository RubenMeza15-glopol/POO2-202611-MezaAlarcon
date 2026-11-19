
# ACTIVIDAD 3 - MVC CON OBSERVER
# MODELO: representa a un estudiante.

from dataclasses import dataclass

@dataclass
class Estudiante:
    # Datos personales y académicos.
    codigo: int
    nombre: str
    notas: list[float]
    ppa: float = 0.0
    ciclo: int = 0

    # Calcula y actualiza el promedio simple de sus notas.
    def calcular_ppa(self):
        if self.notas:
            self.ppa = sum(self.notas) / len(self.notas)
        return self.ppa
