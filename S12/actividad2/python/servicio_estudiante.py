
# =====================================================
# ACTIVIDAD 1: PATRON OBSERVER - PYTHON 3.12
# Servicio encargado de gestionar estudiantes.
# =====================================================

# Importa el estudiante.
from estudiante import Estudiante

# Importa el repositorio observable.
from observer import RepositorioObservable


class ServicioEstudiante:

    # Recibe el repositorio que utilizará el servicio.
    def __init__(self, repositorio: RepositorioObservable):

        # Guarda la referencia al repositorio.
        self.repositorio = repositorio

    # Registra un estudiante.
    def registrar(self, estudiante: Estudiante) -> None:

        # Informa que se inicia el registro.
        print("\nRegistrando estudiante...")

        # Delega el guardado al repositorio.
        # El repositorio notificará automáticamente
        # a LoggerObserver y ConsolaObserver.
        self.repositorio.guardar(estudiante)

    # Consulta un estudiante por su código.
    def consultar(self, codigo: int) -> None:

        # Solicita la búsqueda al repositorio.
        estudiante = self.repositorio.buscar(codigo)

        # Comprueba si encontró al estudiante.
        if estudiante is not None:

            print(f"\nEstudiante encontrado: {estudiante}")

        else:

            print("\nError: Estudiante no encontrado.")

    # Muestra la cantidad de estudiantes registrados.
    def total_estudiantes(self) -> int:

        return len(self.repositorio.listar())
