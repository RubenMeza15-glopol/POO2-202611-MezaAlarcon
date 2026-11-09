# Importa ABC y abstractmethod.
from abc import ABC, abstractmethod

# Importa los repositorios concretos.
from .memoria import RepositorioMemoria
from .archivo import RepositorioArchivo
from .base_datos import RepositorioBD

# Define el creador abstracto.
class CreadorRepositorio(ABC):

    # Declara el método de creación obligatorio.
    @abstractmethod
    def crear_repositorio(self):
        pass

# Define la fábrica concreta para memoria.
class CreadorMemoria(CreadorRepositorio):

    # Crea y devuelve un repositorio en memoria.
    def crear_repositorio(self):
        return RepositorioMemoria()

# Define la fábrica concreta para archivos.
class CreadorArchivo(CreadorRepositorio):

    # Crea y devuelve un repositorio JSON.
    def crear_repositorio(self):
        return RepositorioArchivo()

# Define la fábrica concreta para SQLite.
class CreadorBD(CreadorRepositorio):

    # Crea y devuelve un repositorio de base de datos.
    def crear_repositorio(self):
        return RepositorioBD()