
# SEMANA 13 - ACTIVIDAD 1
# PRUEBA DE PERSISTENCIA REAL CON JSON.

# Importa el sistema operativo para eliminar el archivo de prueba.
import os

# Importa el repositorio JSON.
from repositorio_json import RepositorioJSON

# Importa el modelo Estudiante.
from estudiante import Estudiante

# Define la ruta del archivo JSON de prueba.
RUTA = "estudiantes_test.json"


# Define la función que prueba la persistencia.
def test_persistencia_entre_instancias():

    # PRIMERA INSTANCIA: crear el repositorio.
    r1 = RepositorioJSON(RUTA)

    # Registrar a Ana Quispe.
    r1.guardar(
        Estudiante(1001, "Ana Quispe", 15.5, [14.0, 18.0, 14.5])
    )

    # Registrar a Juan Mamani.
    r1.guardar(
        Estudiante(1002, "Juan Mamani", 12.0, [10.0, 12.0, 14.0])
    )

    # SEGUNDA INSTANCIA: crear otro repositorio.
    # Debe recuperar los datos guardados anteriormente.
    r2 = RepositorioJSON(RUTA)

    # Buscar a Ana por su código.
    ana = r2.buscar(1001)

    # Comprobar que Ana existe.
    assert ana is not None

    # Comprobar su nombre.
    assert ana.nombre == "Ana Quispe"

    # Comprobar su PPA.
    assert abs(ana.ppa - 15.5) < 0.01

    # Buscar a Juan por su código.
    juan = r2.buscar(1002)

    # Comprobar que Juan existe.
    assert juan is not None

    # Comprobar que hay dos estudiantes.
    assert len(r2.listar()) == 2

   
    # Comprobar que hay dos estudiantes.
    assert len(r2.listar()) == 2

    print("Persistencia verificada.")

    # Eliminar a Ana.
    r2.eliminar(1001)

    # Comprobar que Ana ya no existe.
    assert r2.buscar(1001) is None

    # Comprobar que Juan sigue registrado.
    assert r2.buscar(1002) is not None

    # Comprobar que queda un estudiante.
    assert len(r2.listar()) == 1

    # Crear una tercera instancia.
    r3 = RepositorioJSON(RUTA)

    # Comprobar que la eliminación persistió.
    assert r3.buscar(1001) is None
    assert r3.buscar(1002) is not None
    assert len(r3.listar()) == 1

    print("Eliminacion JSON verificada.")

    # Eliminar el archivo temporal.
    os.remove(RUTA)


# Ejecutar la prueba directamente.
if __name__ == "__main__":
    test_persistencia_entre_instancias()
    print("PRUEBA COMPLETA FINALIZADA.")
