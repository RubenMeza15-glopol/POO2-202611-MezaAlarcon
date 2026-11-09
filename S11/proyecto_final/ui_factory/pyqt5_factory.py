# Importa los contratos abstractos.
from .fabrica_ui import Ventana, Menu, Tabla, UIFactory

# Implementa una ventana de la familia PyQt5.
class VentanaPyQt5(Ventana):

    # Simula la presentación de la ventana.
    def mostrar(self):
        return "Ventana PyQt5 creada"

# Implementa un menú de la familia PyQt5.
class MenuPyQt5(Menu):

    # Simula la presentación del menú.
    def mostrar(self):
        return "Menu PyQt5 creado"

# Implementa una tabla de la familia PyQt5.
class TablaPyQt5(Tabla):

    # Simula la presentación de la tabla.
    def mostrar(self):
        return "Tabla PyQt5 creada"

# Implementa la fábrica concreta PyQt5.
class UIFactoryPyQt5(UIFactory):

    # Crea y devuelve una ventana PyQt5.
    def crear_ventana(self):
        return VentanaPyQt5()

    # Crea y devuelve un menú PyQt5.
    def crear_menu(self):
        return MenuPyQt5()

    # Crea y devuelve una tabla PyQt5.
    def crear_tabla(self):
        return TablaPyQt5()