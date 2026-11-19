
# ACTIVIDAD 3 - MVC CON OBSERVER
# MODELO: repositorio que almacena estudiantes.

from estudiante import Estudiante

class RepositorioMemoria:
    # Inicializa la lista de estudiantes.
    def __init__(self):
        self.estudiantes = []

    # Guarda un estudiante en memoria.
    def guardar(self, estudiante: Estudiante):
        self.estudiantes.append(estudiante)

    # Busca un estudiante mediante su código.
    def buscar(self, codigo: int):
        for estudiante in self.estudiantes:
            if estudiante.codigo == codigo:
                return estudiante
        return None

    # Devuelve todos los estudiantes registrados.
    def listar(self):
        return self.estudiantes.copy()
