# Importa ABC para crear clases abstractas.
from abc import ABC, abstractmethod

# Define el producto abstracto Ventana.
class Ventana(ABC):

    # Obliga a implementar el método mostrar.
    @abstractmethod
    def mostrar(self):
        pass

# Define el producto abstracto Menu.
class Menu(ABC):

    # Obliga a implementar el método mostrar.
    @abstractmethod
    def mostrar(self):
        pass

# Define el producto abstracto Tabla.
class Tabla(ABC):

    # Obliga a implementar el método mostrar.
    @abstractmethod
    def mostrar(self):
        pass

# Define la fábrica abstracta de interfaces.
class UIFactory(ABC):

    # Declara el método para crear ventanas.
    @abstractmethod
    def crear_ventana(self):
        pass

    # Declara el método para crear menús.
    @abstractmethod
    def crear_menu(self):
        pass

    # Declara el método para crear tablas.
    @abstractmethod
    def crear_tabla(self):
        pass
    