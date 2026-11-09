# Importa las fábricas concretas.
from factory.fabrica import (
    CreadorMemoria,
    CreadorArchivo,
    CreadorBD
)

# Importa los tipos concretos de repositorio.
from factory.memoria import RepositorioMemoria
from factory.archivo import RepositorioArchivo
from factory.base_datos import RepositorioBD


# Comprueba la creación del repositorio en memoria.
def test_fabrica_memoria():

    # Crea la fábrica de memoria.
    fabrica = CreadorMemoria()

    # Solicita la creación del repositorio.
    repositorio = fabrica.crear_repositorio()

    # Verifica que sea del tipo esperado.
    assert isinstance(repositorio, RepositorioMemoria)


# Comprueba la creación del repositorio de archivo.
def test_fabrica_archivo(tmp_path):

    # Define un archivo temporal para la prueba.
    ruta = tmp_path / "estudiantes.json"

    # Crea la fábrica de archivos.
    fabrica = CreadorArchivo()

    # Crea el repositorio utilizando una ruta temporal.
    repositorio = RepositorioArchivo(str(ruta))

    # Verifica que sea del tipo esperado.
    assert isinstance(repositorio, RepositorioArchivo)


# Comprueba la creación del repositorio SQLite.
def test_fabrica_bd(tmp_path):

    # Define una base de datos temporal.
    ruta = tmp_path / "prueba.db"

    # Crea el repositorio SQLite.
    repositorio = RepositorioBD(str(ruta))

    # Verifica que sea del tipo esperado.
    assert isinstance(repositorio, RepositorioBD)