
# SEMANA 13 - ACTIVIDAD 3
# PRUEBA DE SUSTITUCION DE REPOSITORIOS

# Importa pytest para ejecutar las pruebas.
import pytest

# Importa os para eliminar archivos temporales.
import os

# Importa el servicio de estudiantes.
from servicio_estudiante import ServicioEstudiante

# Importa la estrategia de promedio simple.
from estrategias import PromedioSimple

# Importa el modelo Estudiante.
from estudiante import Estudiante

# Importa los cuatro repositorios.
from repositorio_memoria import RepositorioMemoria
from repositorio_json import RepositorioJSON
from repositorio_csv import RepositorioCSV
from repositorio_sqlite import RepositorioSQLite


# Define cuatro repositorios y sus archivos temporales.
@pytest.mark.parametrize(
    "RepoClass, kwargs, cleanup",
    [
        (RepositorioMemoria, {}, None),
        (RepositorioJSON, {"ruta": "test.json"}, "test.json"),
        (RepositorioCSV, {"ruta": "test.csv"}, "test.csv"),
        (RepositorioSQLite, {"ruta": "test.db"}, "test.db"),
    ]
)

# Prueba el servicio con cada repositorio.
def test_servicio_con_cualquier_repo(
    RepoClass, kwargs, cleanup
):

    # Crea el repositorio correspondiente.
    repo = RepoClass(**kwargs)

    # Crea el servicio con promedio simple.
    svc = ServicioEstudiante(repo, PromedioSimple())

    # Crea el primer estudiante.
    e1 = Estudiante(
        1001,
        "Ana",
        0.0,
        [15.0, 18.0, 14.0]
    )

    # Crea el segundo estudiante.
    e2 = Estudiante(
        1002,
        "Juan",
        0.0,
        [10.0, 12.0, 14.0]
    )

    # Registra los dos estudiantes.
    svc.registrar(e1)
    svc.registrar(e2)

    # Comprueba que Ana fue guardada.
    assert svc.buscar(1001).nombre == "Ana"

    # Comprueba que Juan existe.
    assert svc.buscar(1002) is not None

    # Comprueba que existen dos estudiantes.
    assert len(svc.listar()) == 2

    # Comprueba el promedio simple de Ana.
    assert abs(svc.buscar(1001).ppa - (47 / 3)) < 0.01

    # Cierra SQLite si corresponde.
    if isinstance(repo, RepositorioSQLite):
        repo.cerrar()

    # Elimina el archivo temporal si corresponde.
    if cleanup and os.path.exists(cleanup):
        os.remove(cleanup)
