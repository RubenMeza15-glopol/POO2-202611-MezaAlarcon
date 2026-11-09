# Importa el Logger del patrón Singleton.
from singleton.logger import Logger

# Importa la Configuración del patrón Singleton.
from singleton.config import Config

# Importa las fábricas de repositorios.
from factory.fabrica import (
    CreadorMemoria,
    CreadorArchivo,
    CreadorBD
)

# Importa la fábrica de interfaz Tkinter.
from ui_factory.tkinter_factory import UIFactoryTkinter

# Importa la fábrica de interfaz PyQt5.
from ui_factory.pyqt5_factory import UIFactoryPyQt5


# Define la función principal del programa.
def main():

    # Obtiene la instancia única del Logger.
    logger = Logger()

    # Obtiene la instancia única de Config.
    config = Config()

    # Muestra el nombre del sistema.
    print(config.obtener("APP_NOMBRE"))

    # Registra el inicio del programa.
    logger.info("MAIN", "Sistema iniciado")

    # Crea la fábrica de repositorios en memoria.
    fabrica = CreadorMemoria()

    # Solicita la creación del repositorio.
    repositorio = fabrica.crear_repositorio()

    # Registra un estudiante.
    repositorio.guardar("Maria Quispe")

    # Muestra los estudiantes registrados.
    print("Estudiantes:", repositorio.listar())

    # Crea la fábrica de componentes Tkinter.
    tkinter = UIFactoryTkinter()

    # Muestra los componentes Tkinter.
    print(tkinter.crear_ventana().mostrar())
    print(tkinter.crear_menu().mostrar())
    print(tkinter.crear_tabla().mostrar())

    # Crea la fábrica de componentes PyQt5.
    pyqt = UIFactoryPyQt5()

    # Muestra los componentes PyQt5.
    print(pyqt.crear_ventana().mostrar())
    print(pyqt.crear_menu().mostrar())
    print(pyqt.crear_tabla().mostrar())

    # Registra la finalización del programa.
    logger.info("MAIN", "Sistema finalizado")


# Comprueba si el archivo se ejecuta directamente.
if __name__ == "__main__":

    # Ejecuta la función principal.
    main()