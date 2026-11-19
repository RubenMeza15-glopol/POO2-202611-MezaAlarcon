
# SEMANA 13 - ACTIVIDAD 3
# ESTRATEGIAS DE CALCULO

# Define el cálculo del promedio simple.
class PromedioSimple:

    # Calcula el promedio de las notas.
    def calcular(self, notas: list[float]) -> float:

        # Si no hay notas, devuelve cero.
        if not notas:
            return 0.0

        # Suma las notas y divide entre su cantidad.
        return sum(notas) / len(notas)
