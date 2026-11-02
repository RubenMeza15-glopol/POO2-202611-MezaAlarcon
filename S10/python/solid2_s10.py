
# ================================================================
# CURSO: PROGRAMACIÓN ORIENTADA A OBJETOS II - POO II
# UNIDAD: SEGUNDA UNIDAD
# SEMANA: 10
# ACTIVIDAD 1B Y 2B: SRP Y OCP EN PYTHON 3.12
#
# ACTIVIDAD 2B - PREGUNTA DEL INGENIERO:
# Agregar PromedioModerado en solid_s10.py.
# Crear svc2 = ServicioEstudiante(repo, PromedioModerado()).
# Registrar el mismo estudiante y comparar ambos PPA.
#
# PREGUNTA FINAL:
# ¿ServicioEstudiante cambió?
#
# RESOLUCIÓN:
# Incorporamos una nueva estrategia de cálculo sin modificar
# la clase ServicioEstudiante. Esto demuestra el principio OCP.
# ================================================================

# Permite crear clases destinadas a almacenar datos.
from dataclasses import dataclass, field

# Permite definir tipos e interfaces para las clases.
from typing import Optional, Protocol, Sequence


# ================================================================
# 1. CLASE ESTUDIANTE
# RESPONSABILIDAD: almacenar los datos del estudiante.
# ================================================================

@dataclass
class Estudiante:

    # Código único del estudiante.
    codigo: int

    # Nombre completo del estudiante.
    nombre: str

    # Promedio ponderado académico.
    ppa: float = 0.0

    # Lista de notas del estudiante.
    notas: list[float] = field(default_factory=list)


# ================================================================
# 2. INTERFAZ Y ESTRATEGIAS DE CÁLCULO
# RESPONSABILIDAD: realizar diferentes tipos de promedio.
# ================================================================

class IEstrategiaCalculo(Protocol):

    # Contrato que deben cumplir las estrategias de cálculo.
    def calcular(self, notas: Sequence[float]) -> float:
        ...


# -------------------- PROMEDIO SIMPLE ----------------------------

class PromedioSimple:

    # Calcula el promedio utilizando todas las notas.
    def calcular(self, notas: Sequence[float]) -> float:

        # Si existen notas, suma y divide entre su cantidad.
        # Si no existen, devuelve cero.
        return sum(notas) / len(notas) if notas else 0.0


# -------------------- PROMEDIO MODERADO --------------------------

class PromedioModerado:

    # Calcula el promedio descartando la nota mayor y menor.
    def calcular(self, notas: Sequence[float]) -> float:

        # Necesitamos al menos tres notas.
        if len(notas) < 3:
            raise ValueError(
                "Se necesitan al menos tres notas."
            )

        # Ordenamos las notas de menor a mayor.
        notas_ordenadas = sorted(notas)

        # Quitamos la primera nota (menor) y la última (mayor).
        notas_centrales = notas_ordenadas[1:-1]

        # Calculamos el promedio de las notas restantes.
        return sum(notas_centrales) / len(notas_centrales)


# ================================================================
# 3. REPOSITORIO
# RESPONSABILIDAD: guardar, buscar y listar estudiantes.
# ================================================================

class IRepositorioEstudiante(Protocol):

    # Contrato para guardar un estudiante.
    def guardar(self, e: Estudiante) -> None:
        ...

    # Contrato para buscar un estudiante por código.
    def buscar(self, cod: int) -> Optional[Estudiante]:
        ...

    # Contrato para listar los estudiantes.
    def listar(self) -> list[Estudiante]:
        ...


class RepositorioMemoria:

    # Inicializa el diccionario que almacenará estudiantes.
    def __init__(self) -> None:
        self._datos: dict[int, Estudiante] = {}

    # Guarda al estudiante utilizando su código.
    def guardar(self, e: Estudiante) -> None:
        self._datos[e.codigo] = e

    # Busca y devuelve al estudiante si existe.
    def buscar(self, cod: int) -> Optional[Estudiante]:
        return self._datos.get(cod)

    # Devuelve todos los estudiantes almacenados.
    def listar(self) -> list[Estudiante]:
        return list(self._datos.values())


# ================================================================
# 4. SERVICIO ESTUDIANTE
# RESPONSABILIDAD: coordinar el cálculo y almacenamiento.
# ================================================================

class ServicioEstudiante:

    # Recibe un repositorio y una estrategia de cálculo.
    def __init__(
        self,
        repo: IRepositorioEstudiante,
        calc: IEstrategiaCalculo
    ) -> None:

        # Almacena el repositorio recibido.
        self._repo = repo

        # Almacena la estrategia de cálculo recibida.
        self._calc = calc

    # Registra al estudiante calculando automáticamente su PPA.
    def registrar(self, e: Estudiante) -> None:

        # Utiliza la estrategia que recibió el servicio.
        e.ppa = self._calc.calcular(e.notas)

        # Guarda al estudiante con su promedio actualizado.
        self._repo.guardar(e)

    # Busca un estudiante por su código.
    def buscar(self, cod: int) -> Optional[Estudiante]:
        return self._repo.buscar(cod)


# ================================================================
# 5. PROGRAMA PRINCIPAL
# ACTIVIDAD 1B: registrar tres estudiantes y verificar sus PPA.
# ================================================================

def main():

    print("=" * 60)
    print("ACTIVIDAD 1B - IMPLEMENTACIÓN SRP EN PYTHON 3.12")
    print("=" * 60)

    # Creamos el repositorio en memoria.
    repositorio = RepositorioMemoria()

    # Creamos la estrategia de promedio simple.
    estrategia = PromedioSimple()

    # Creamos el servicio con repositorio y promedio simple.
    servicio = ServicioEstudiante(repositorio, estrategia)

    # Creamos tres estudiantes con notas diferentes.
    estudiante1 = Estudiante(
        1001, "Ana Quispe", notas=[15, 16, 17]
    )

    estudiante2 = Estudiante(
        1002, "Luis Mamani", notas=[12, 14, 18]
    )

    estudiante3 = Estudiante(
        1003, "Rosa Condori", notas=[16, 18, 20]
    )

    # Registramos a los tres estudiantes.
    servicio.registrar(estudiante1)
    servicio.registrar(estudiante2)
    servicio.registrar(estudiante3)

    # Verificamos los estudiantes mediante buscar().
    print("\nVERIFICACION MEDIANTE BUSCAR()")

    for codigo in [1001, 1002, 1003]:

        # Buscamos al estudiante por su código.
        estudiante = servicio.buscar(codigo)

        # Comprobamos si fue encontrado.
        if estudiante is not None:

            # Mostramos sus datos y promedio.
            print(f"\nCodigo: {estudiante.codigo}")
            print(f"Nombre: {estudiante.nombre}")
            print(f"Notas: {estudiante.notas}")
            print(f"PPA calculado: {estudiante.ppa:.2f}")

    # ============================================================
    # ACTIVIDAD 2B - PRINCIPIO OCP EN PYTHON 3.12
    #
    # PREGUNTA DEL INGENIERO:
    # Agregar PromedioModerado y utilizarlo desde ServicioEstudiante
    # sin modificar la clase ServicioEstudiante.
    #
    # ¿QUE NOS PIDE REALIZAR?
    # 1. Crear una nueva estrategia de promedio moderado.
    # 2. Crear svc2 con el mismo repositorio y nueva estrategia.
    # 3. Registrar el mismo estudiante con ambas estrategias.
    # 4. Comparar los resultados de los dos PPA.
    # ============================================================

    print("\n" + "=" * 60)
    print("ACTIVIDAD 2B - PRINCIPIO OCP")
    print("=" * 60)

    # Utilizamos las mismas notas para comparar ambas estrategias.
    notas_prueba = [10, 14, 16, 18, 20]

    # Creamos el estudiante de prueba para el promedio simple.
    estudiante_simple = Estudiante(
        1004, "Carlos Ramos", notas=notas_prueba.copy()
    )

    # Registramos al estudiante utilizando PromedioSimple.
    servicio.registrar(estudiante_simple)

    # Guardamos el resultado del promedio simple.
    ppa_simple = estudiante_simple.ppa

    # Mostramos el resultado de la primera estrategia.
    print("\nRESULTADO CON PROMEDIO SIMPLE")
    print(f"Notas: {notas_prueba}")
    print(f"PPA simple: {ppa_simple:.2f}")

    # ------------------------------------------------------------
    # NUEVA ESTRATEGIA: PROMEDIO MODERADO
    # ------------------------------------------------------------

    # Creamos svc2 utilizando el mismo repositorio,
    # pero ahora con la estrategia PromedioModerado.
    svc2 = ServicioEstudiante(repositorio, PromedioModerado())

    # Creamos el mismo estudiante con los mismos datos y notas.
    estudiante_moderado = Estudiante(
        1004, "Carlos Ramos", notas=notas_prueba.copy()
    )

    # Registramos al estudiante utilizando la nueva estrategia.
    svc2.registrar(estudiante_moderado)

    # Mostramos el resultado del promedio moderado.
    print("\nRESULTADO CON PROMEDIO MODERADO")
    print(f"Notas: {notas_prueba}")
    print("Se descarta la nota menor: 10")
    print("Se descarta la nota mayor: 20")
    print(f"PPA moderado: {estudiante_moderado.ppa:.2f}")

    # ------------------------------------------------------------
    # COMPARACIÓN DE RESULTADOS
    # ------------------------------------------------------------

    print("\nCOMPARACION FINAL")
    print(f"Promedio simple: {ppa_simple:.2f}")
    print(f"Promedio moderado: {estudiante_moderado.ppa:.2f}")

    # ------------------------------------------------------------
    # RESPUESTA A LA PREGUNTA DEL INGENIERO:
    # ¿ServicioEstudiante cambió?
    #
    # RESPUESTA: NO.
    #
    # No modificamos la clase ServicioEstudiante.
    # Solamente agregamos una nueva estrategia llamada
    # PromedioModerado y la inyectamos en el servicio.
    #
    # Esto demuestra OCP:
    # ABIERTO PARA EXTENSIÓN Y CERRADO PARA MODIFICACIÓN.
    # ------------------------------------------------------------

    print("\n¿ServicioEstudiante cambio? NO.")
    print("Se agrego una nueva estrategia sin modificar el servicio.")

    print("\nActividad 1B y 2B finalizadas correctamente.")


# Ejecutamos main cuando iniciamos directamente este archivo.
if __name__ == "__main__":
    main()
