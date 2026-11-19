# SEMANA 14 - ESTRATEGIAS DE PROMEDIO

class PromedioSimple:

    def calcular(self, notas: list[float]) -> float:

        if not notas:
            raise ValueError("Debe ingresar notas.")

        return sum(notas) / len(notas)


class PromedioModerado:

    def calcular(self, notas: list[float]) -> float:

        if len(notas) < 3:
            raise ValueError(
                "Se necesitan al menos tres notas."
            )

        ordenadas = sorted(notas)

        # Elimina la nota menor y la mayor.
        centrales = ordenadas[1:-1]

        return sum(centrales) / len(centrales)