
# SEMANA 13 - ACTIVIDAD 2
# REPOSITORIO CSV CON PERSISTENCIA.

# Importa las herramientas para leer y escribir CSV.
import csv

# Permite trabajar con rutas de archivos.
import pathlib

# Permite convertir listas de notas a texto JSON y viceversa.
import json

# Permite indicar que una búsqueda puede devolver None.
from typing import Optional

# Importa el modelo Estudiante.
from estudiante import Estudiante


# Define las columnas del archivo CSV.
CAMPOS = ["codigo", "nombre", "ppa", "notas"]


# Clase encargada de guardar estudiantes en CSV.
class RepositorioCSV:

    # Constructor: recibe la ruta del archivo.
    def __init__(self, ruta: str) -> None:

        # Convierte la ruta en un objeto Path.
        self._ruta = pathlib.Path(ruta)

        # Diccionario de estudiantes identificados por código.
        self._datos: dict[int, Estudiante] = {}

        # Carga los datos si el archivo ya existe.
        self._cargar()

    # Carga los estudiantes desde el CSV.
    def _cargar(self) -> None:

        # Si el archivo no existe, termina.
        if not self._ruta.exists():
            return

        # Abre el archivo en modo lectura.
        with self._ruta.open(
            newline="",
            encoding="utf-8"
        ) as f:

            # Lee las filas utilizando sus encabezados.
            for row in csv.DictReader(f):

                # Convierte cada fila en un objeto Estudiante.
                e = Estudiante(
                    int(row["codigo"]),
                    row["nombre"],
                    float(row["ppa"]),
                    json.loads(row["notas"])
                )

                # Guarda el estudiante en el diccionario.
                self._datos[e.codigo] = e

    # Persiste todos los estudiantes en el CSV.
    def _persistir(self) -> None:

        # Abre el archivo en modo escritura.
        with self._ruta.open(
            "w",
            newline="",
            encoding="utf-8"
        ) as f:

            # Crea el escritor con los nombres de columnas.
            w = csv.DictWriter(f, fieldnames=CAMPOS)

            # Escribe el encabezado.
            w.writeheader()

            # Recorre los estudiantes registrados.
            for e in self._datos.values():

                # Escribe cada estudiante como una fila.
                w.writerow({
                    "codigo": e.codigo,
                    "nombre": e.nombre,
                    "ppa": e.ppa,
                    "notas": json.dumps(e.notas)
                })

    # Registra un estudiante y guarda el CSV.
    def guardar(self, e: Estudiante) -> None:

        # Almacena el estudiante por su código.
        self._datos[e.codigo] = e

        # Actualiza el archivo CSV.
        self._persistir()

    # Busca un estudiante por su código.
    def buscar(self, cod: int) -> Optional[Estudiante]:

        # Devuelve el estudiante o None si no existe.
        return self._datos.get(cod)

    # Devuelve todos los estudiantes.
    def listar(self) -> list[Estudiante]:

        # Convierte los valores del diccionario en lista.
        return list(self._datos.values())
