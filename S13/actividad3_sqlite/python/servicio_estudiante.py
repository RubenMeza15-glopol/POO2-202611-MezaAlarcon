
# SEMANA 13 - ACTIVIDAD 3
# SERVICIO DE ESTUDIANTES

# Importa el modelo.
from estudiante import Estudiante


# Servicio que administra estudiantes.
class ServicioEstudiante:

    # Recibe un repositorio y una estrategia de promedio.
    def __init__(self, repo, calculadora):

        # Guarda el repositorio recibido.
        self.repo = repo

        # Guarda la estrategia de cálculo.
        self.calculadora = calculadora

    # Registra un estudiante.
    def registrar(self, estudiante: Estudiante) -> None:

        # Calcula el PPA usando la estrategia.
        estudiante.ppa = self.calculadora.calcular(
            estudiante.notas
        )

        # Guarda el estudiante en el repositorio.
        self.repo.guardar(estudiante)

    # Busca un estudiante por código.
    def buscar(self, codigo: int):

        # Delega la búsqueda al repositorio.
        return self.repo.buscar(codigo)

    # Lista los estudiantes.
    def listar(self):

        # Delega el listado al repositorio.
        return self.repo.listar()
