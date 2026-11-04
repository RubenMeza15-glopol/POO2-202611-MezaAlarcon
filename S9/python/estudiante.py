
# ACTIVIDAD 2B: Implementar y probar Estudiante en Python 3.12
# Pregunta: ¿Podemos representar y validar un estudiante usando dataclasses?

# Importamos dataclass para crear clases que almacenan datos automáticamente.
from dataclasses import dataclass, field, asdict

# Importamos Optional para indicar que una función puede devolver un número o None.
from typing import Optional

# Importamos json para convertir los datos del estudiante en formato JSON.
import json


# @dataclass genera automáticamente métodos básicos de la clase.
@dataclass
class Estudiante:

    # Atributos que representan los datos del estudiante.
    codigo: int                  # Código único del estudiante.
    nombre: str                  # Nombre completo del estudiante.
    ppa: float                   # Promedio ponderado acumulado.
    ciclo: int                   # Ciclo académico del estudiante.

    # Lista de notas; cada objeto tendrá su propia lista independiente.
    notas: list[float] = field(default_factory=list)

    # __post_init__ se ejecuta después del constructor automático.
    def __post_init__(self):

        # Validamos que el código sea positivo.
        if self.codigo <= 0:
            raise ValueError("El código debe ser positivo")

        # Validamos que el nombre no esté vacío.
        if not self.nombre.strip():
            raise ValueError("El nombre no puede estar vacío")

        # Validamos que el PPA esté entre 0 y 20.
        if not (0.0 <= self.ppa <= 20.0):
            raise ValueError("El PPA debe estar entre 0 y 20")

        # Validamos que el ciclo sea positivo.
        if self.ciclo <= 0:
            raise ValueError("El ciclo debe ser positivo")

        # Validamos que todas las notas estén entre 0 y 20.
        for nota in self.notas:
            if not (0.0 <= nota <= 20.0):
                raise ValueError("Existe una nota fuera de rango")

    # Método para agregar una nota al estudiante.
    def agregar_nota(self, nota: float) -> None:

        # Comprobamos que la nota esté dentro del rango permitido.
        if not (0.0 <= nota <= 20.0):
            raise ValueError("Nota fuera de rango")

        # Agregamos la nota al final de la lista.
        self.notas.append(nota)

    # Método que calcula el promedio de las notas.
    def calcular_promedio(self) -> Optional[float]:

        # Si no existen notas, devolvemos None.
        if not self.notas:
            return None

        # Sumamos todas las notas y dividimos entre su cantidad.
        return sum(self.notas) / len(self.notas)

    # Método especial para mostrar los datos como texto.
    def __str__(self) -> str:

        # Construimos una cadena con los datos del estudiante.
        return (
            f"[{self.codigo}] {self.nombre} - "
            f"PPA: {self.ppa} - Ciclo: {self.ciclo}"
        )


# Este bloque se ejecuta únicamente cuando abrimos este archivo directamente.
if __name__ == "__main__":

    # Creamos un estudiante con sus datos iniciales.
    e = Estudiante(1001, "Ana Quispe", 15.5, 3)

    # Registramos cinco notas diferentes.
    for nota in [14.0, 16.0, 18.0, 15.0, 17.0]:

        # Enviamos cada nota al método agregar_nota.
        e.agregar_nota(nota)

    # Mostramos los datos generales del estudiante.
    print(e)

    # Calculamos el promedio y mostramos dos decimales.
    print(f"Promedio semestral: {e.calcular_promedio():.2f}")

    # ------------------------------------------------
    # PRUEBAS DE VALIDACIÓN SOLICITADAS POR LA ACTIVIDAD
    # ------------------------------------------------

    # Prueba 1: verificamos que no se acepte un código negativo.
    try:
        Estudiante(-1, "X", 15.0, 1)
        assert False, "Debió rechazarse el código inválido"
    except ValueError:
        print("Prueba 1 correcta: código inválido rechazado")

    # Prueba 2: verificamos que no se acepte un nombre vacío.
    try:
        Estudiante(1002, "", 15.0, 1)
        assert False, "Debió rechazarse el nombre vacío"
    except ValueError:
        print("Prueba 2 correcta: nombre inválido rechazado")

    # Prueba 3: verificamos que no se acepte un PPA mayor que 20.
    try:
        Estudiante(1003, "Luis Mamani", 21.0, 2)
        assert False, "Debió rechazarse el PPA inválido"
    except ValueError:
        print("Prueba 3 correcta: PPA inválido rechazado")

    # ------------------------------------------------
    # ACTIVIDAD ADICIONAL: SERIALIZACIÓN JSON
    # ------------------------------------------------

    # Convertimos el objeto Estudiante en un diccionario.
    datos = asdict(e)

    # Convertimos el diccionario a una cadena JSON legible.
    resultado_json = json.dumps(datos, indent=4, ensure_ascii=False)

    # Mostramos la información serializada.
    print("\nDatos del estudiante en formato JSON:")
    print(resultado_json)
