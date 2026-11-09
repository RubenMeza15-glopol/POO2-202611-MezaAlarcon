# Importa los contratos abstractos.
from .fabrica_ui import Ventana, Menu, Tabla, UIFactory

# Implementa una ventana de la familia Tkinter.
class VentanaTkinter(Ventana):

    # Simula la presentación de la ventana.
    def mostrar(self):
        return "Ventana Tkinter creada"

# Implementa un menú de la familia Tkinter.
class MenuTkinter(Menu):

    # Simula la presentación del menú.
    def mostrar(self):
        return "Menu Tkinter creado"

# Implementa una tabla de la familia Tkinter.
class TablaTkinter(Tabla):

    # Simula la presentación de la tabla.
    def mostrar(self):
        return "Tabla Tkinter creada"

# Implementa la fábrica concreta Tkinter.
class UIFactoryTkinter(UIFactory):

    # Crea y devuelve una ventana Tkinter.
    def crear_ventana(self):
        return VentanaTkinter()

    # Crea y devuelve un menú Tkinter.
    def crear_menu(self):
        return MenuTkinter()

    # Crea y devuelve una tabla Tkinter.
    def crear_tabla(self):
        return TablaTkinter()