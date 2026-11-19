
# ACTIVIDAD 3 - MVC CON OBSERVER
# CONTROLADOR: administra las operaciones de estudiantes.

# Importa el modelo Estudiante.
from estudiante import Estudiante

# Importa el repositorio observable.
from observer import RepositorioObservable

# Importa las estrategias de promedio.
from estrategias import EstrategiaPromedio


class ServicioEstudiante:

    # Recibe el repositorio y la estrategia inicial.
    def __init__(
        self,
        repositorio: RepositorioObservable,
        estrategia: EstrategiaPromedio
    ):
        # Guarda el repositorio que utilizará.
        self.repositorio = repositorio

        # Guarda la estrategia de cálculo seleccionada.
        self.estrategia = estrategia

    # Permite cambiar la estrategia durante la ejecución.
    def cambiar_estrategia(self, nueva_estrategia: EstrategiaPromedio):
        self.estrategia = nueva_estrategia

    # Registra un estudiante y calcula su PPA.
    def registrar(self, estudiante: Estudiante):
        # Calcula el promedio utilizando la estrategia actual.
        estudiante.ppa = self.estrategia.calcular(estudiante.notas)

        # Guarda al estudiante y activa las notificaciones.
        self.repositorio.guardar(estudiante)

    # Consulta un estudiante por su código.
    def consultar(self, codigo: int):
        return self.repositorio.buscar(codigo)

    # Devuelve la cantidad de estudiantes registrados.
    def total_estudiantes(self):
        return len(self.repositorio.listar())
