
# ================================================================
# CURSO: PROGRAMACIÓN ORIENTADA A OBJETOS II - POO II
# UNIDAD: SEGUNDA UNIDAD
# SEMANA: 10
# ACTIVIDAD 1B: IMPLEMENTAR Y PROBAR EN PYTHON 3.12
#
# PREGUNTA DEL INGENIERO:
# Crear un ServicioEstudiante utilizando RepositorioMemoria
# y PromedioSimple.
#
# ¿QUÉ NOS PIDE REALIZAR?
# 1. Registrar tres estudiantes con notas distintas.
# 2. Calcular automáticamente su PPA.
# 3. Verificar mediante buscar() que el PPA sea correcto.
# 4. Implementar PromedioModerado como actividad adicional,
#    descartando la nota mayor y la menor.
#
# RESOLUCIÓN:
# Aplicamos SRP separando los datos, el cálculo, el repositorio
# y la coordinación del sistema en clases independientes.
# ================================================================

# Importamos dataclass para crear clases destinadas a almacenar datos.
from dataclasses import dataclass, field

# Importamos herramientas para indicar tipos de datos e interfaces.
from typing import Optional, Protocol, Sequence


# ================================================================
# 1. CLASE ESTUDIANTE
# RESPONSABILIDAD: almacenar únicamente los datos del estudiante.
# ================================================================

@dataclass
class Estudiante:

    # Código único que identifica al estudiante.
    codigo: int

    # Nombre completo del estudiante.
    nombre: str

    # Promedio ponderado académico, inicialmente cero.
    ppa: float = 0.0

    # Lista que almacena las notas del estudiante.
    notas: list[float] = field(default_factory=list)


# ================================================================
# 2. INTERFAZ Y ESTRATEGIAS DE CÁLCULO
# RESPONSABILIDAD: definir y realizar el cálculo del promedio.
# ================================================================

class IEstrategiaCalculo(Protocol):

    # Define el contrato que deben cumplir las estrategias.
    def calcular(self, notas: Sequence[float]) -> float:
        ...


# -------------------- PROMEDIO SIMPLE ----------------------------

class PromedioSimple:

    # Calcula la media aritmética de todas las notas.
    def calcular(self, notas: Sequence[float]) -> float:

        # Si no existen notas, devuelve cero para evitar división
        # entre cero.
        return sum(notas) / len(notas) if notas else 0.0


# -------------------- PROMEDIO MODERADO --------------------------

class PromedioModerado:

    # Calcula el promedio descartando la nota mayor y la menor.
    def calcular(self, notas: Sequence[float]) -> float:

        # Se necesitan al menos tres notas para descartar dos.
        if len(notas) < 3:
            raise ValueError(
                "Se necesitan al menos tres notas."
            )

        # Ordenamos las notas de menor a mayor.
        notas_ordenadas = sorted(notas)

        # Eliminamos la primera nota (menor) y la última (mayor).
        notas_centrales = notas_ordenadas[1:-1]

        # Calculamos el promedio de las notas restantes.
        return sum(notas_centrales) / len(notas_centrales)


# ================================================================
# 3. REPOSITORIO
# RESPONSABILIDAD: guardar, buscar y listar estudiantes.
# ================================================================

class IRepositorioEstudiante(Protocol):

    # Define la operación para guardar un estudiante.
    def guardar(self, e: Estudiante) -> None:
        ...

    # Define la operación para buscar por código.
    def buscar(self, cod: int) -> Optional[Estudiante]:
        ...

    # Define la operación para listar estudiantes.
    def listar(self) -> list[Estudiante]:
        ...


class RepositorioMemoria:

    # Constructor: crea un diccionario vacío para almacenar datos.
    def __init__(self) -> None:
        self._datos: dict[int, Estudiante] = {}

    # Guarda al estudiante usando su código como identificador.
    def guardar(self, e: Estudiante) -> None:
        self._datos[e.codigo] = e

    # Busca un estudiante y lo devuelve si existe.
    def buscar(self, cod: int) -> Optional[Estudiante]:
        return self._datos.get(cod)

    # Devuelve una lista con todos los estudiantes registrados.
    def listar(self) -> list[Estudiante]:
        return list(self._datos.values())


# ================================================================
# 4. SERVICIO ESTUDIANTE
# RESPONSABILIDAD: coordinar el cálculo y el almacenamiento.
# ================================================================

class ServicioEstudiante:

    # Recibe un repositorio y una estrategia de cálculo.
    # Esto aplica DIP: depende de abstracciones y no de clases
    # concretas directamente.
    def __init__(
        self,
        repo: IRepositorioEstudiante,
        calc: IEstrategiaCalculo
    ) -> None:

        # Guardamos el repositorio recibido.
        self._repo = repo

        # Guardamos la estrategia de cálculo recibida.
        self._calc = calc

    # Registra un estudiante y calcula automáticamente su PPA.
    def registrar(self, e: Estudiante) -> None:

        # Calculamos el promedio utilizando la estrategia elegida.
        e.ppa = self._calc.calcular(e.notas)

        # Guardamos al estudiante con su PPA actualizado.
        self._repo.guardar(e)

    # Busca un estudiante por su código.
    def buscar(self, cod: int) -> Optional[Estudiante]:
        return self._repo.buscar(cod)


# ================================================================
# 5. PROGRAMA PRINCIPAL
# PREGUNTA: registrar tres estudiantes y verificar sus promedios.
# ================================================================

def main():

    print("=" * 55)
    print("ACTIVIDAD 1B - REFACTORIZACIÓN SRP EN PYTHON 3.12")
    print("=" * 55)

    # Creamos el repositorio que almacenará los estudiantes.
    repositorio = RepositorioMemoria()

    # Creamos la estrategia de promedio simple.
    estrategia = PromedioSimple()

    # Creamos el servicio conectando repositorio y estrategia.
    servicio = ServicioEstudiante(repositorio, estrategia)

    # Creamos tres estudiantes con diferentes notas.
    estudiante1 = Estudiante(
        1001, "Ana Quispe", notas=[15, 16, 17]
    )

    estudiante2 = Estudiante(
        1002, "Luis Mamani", notas=[12, 14, 18]
    )

    estudiante3 = Estudiante(
        1003, "Rosa Condori", notas=[16, 18, 20]
    )

    # Registramos los tres estudiantes.
    # El servicio calcula su PPA y los almacena.
    servicio.registrar(estudiante1)
    servicio.registrar(estudiante2)
    servicio.registrar(estudiante3)

    # Buscamos a los estudiantes por sus respectivos códigos.
    print("\nVERIFICACIÓN MEDIANTE BUSCAR()")

    for codigo in [1001, 1002, 1003]:

        # Recuperamos al estudiante del repositorio.
        estudiante = servicio.buscar(codigo)

        # Comprobamos si el estudiante fue encontrado.
        if estudiante is not None:

            # Mostramos sus datos y el promedio calculado.
            print(f"\nCódigo: {estudiante.codigo}")
            print(f"Nombre: {estudiante.nombre}")
            print(f"Notas: {estudiante.notas}")
            print(f"PPA calculado: {estudiante.ppa:.2f}")

    # ============================================================
    # 6. PRUEBA ADICIONAL: PROMEDIO MODERADO
    # PREGUNTA: descartar la nota mayor y menor antes de promediar.
    # ============================================================

    print("\nPRUEBA ADICIONAL - PROMEDIO MODERADO")

    # Creamos la estrategia de promedio moderado.
    promedio_moderado = PromedioModerado()

    # Definimos notas de prueba.
    notas_prueba = [10, 14, 16, 18, 20]

    # Calculamos el promedio descartando el 10 y el 20.
    resultado = promedio_moderado.calcular(notas_prueba)

    # Mostramos las notas originales y el resultado.
    print(f"Notas originales: {notas_prueba}")
    print("Se descarta la nota menor: 10")
    print("Se descarta la nota mayor: 20")
    print(f"Promedio moderado: {resultado:.2f}")

    print("\nActividad 1B finalizada correctamente.")


# Ejecutamos main únicamente cuando este archivo se ejecuta directamente.
if __name__ == "__main__":
    main()
