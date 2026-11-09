# Importa ABC para crear clases abstractas.
from abc import ABC, abstractmethod

# Define la interfaz común de los repositorios.
class Repositorio(ABC):

    # Obliga a implementar el método guardar.
    @abstractmethod
    def guardar(self, estudiante):
        pass

    # Obliga a implementar el método listar.
    @abstractmethod
    def listar(self):
        pass