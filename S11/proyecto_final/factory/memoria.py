# Importa la interfaz del repositorio.
from .repositorio import Repositorio

# Define el repositorio en memoria.
class RepositorioMemoria(Repositorio):

    # Inicializa la lista de estudiantes.
    def __init__(self):
        self.estudiantes = []

    # Guarda un estudiante en la lista.
    def guardar(self, estudiante):
        self.estudiantes.append(estudiante)

    # Devuelve una copia de los estudiantes.
    def listar(self):
        return self.estudiantes.copy()