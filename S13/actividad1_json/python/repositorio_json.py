
# SEMANA 13 - ACTIVIDAD 1
# ARCHIVO: repositorio_json.py
# REPOSITORIO CON PERSISTENCIA JSON.

# Permite trabajar con archivos y rutas.
import json
import pathlib

# Permite convertir diccionarios en objetos Estudiante.
from dataclasses import asdict, fields

# Permite indicar que una búsqueda puede devolver None.
from typing import Optional

# Importa el modelo Estudiante.
from estudiante import Estudiante


# Define el repositorio que almacena estudiantes en JSON.
class RepositorioJSON:

    # Constructor: recibe la ruta del archivo JSON.
    def __init__(self, ruta: str) -> None:

        # Convierte la ruta recibida en un objeto Path.
        self._ruta = pathlib.Path(ruta)

        # Diccionario que almacena estudiantes usando su código.
        self._datos: dict[int, Estudiante] = {}

        # Carga los datos existentes al crear el repositorio.
        self._cargar()

    # Carga los estudiantes desde el archivo JSON.
    def _cargar(self) -> None:

        # Comprueba si el archivo existe.
        if not self._ruta.exists():
            return

        # Abre el archivo en modo lectura y codificación UTF-8.
        with self._ruta.open(encoding="utf-8") as f:

            # Convierte el contenido JSON en una lista de diccionarios.
            lista = json.load(f)

            # Recorre cada registro de la lista.
            for item in lista:

                # Convierte el diccionario en un objeto Estudiante.
                e = Estudiante(**item)

                # Almacena el estudiante usando su código.
                self._datos[e.codigo] = e

    # Guarda todos los estudiantes en el archivo JSON.
    def _persistir(self) -> None:

        # Convierte cada estudiante en un diccionario.
        lista = [asdict(e) for e in self._datos.values()]

        # Abre el archivo en modo escritura.
        with self._ruta.open("w", encoding="utf-8") as f:

            # Escribe los datos en formato JSON legible.
            json.dump(
                lista,
                f,
                indent=2,
                ensure_ascii=False
            )

    # Registra un estudiante y guarda los cambios.
    def guardar(self, e: Estudiante) -> None:

        # Almacena el estudiante en el diccionario.
        self._datos[e.codigo] = e

        # Actualiza el archivo JSON.
        self._persistir()

    # Busca un estudiante por su código.
    def buscar(self, cod: int) -> Optional[Estudiante]:

        # Devuelve el estudiante o None si no existe.
        return self._datos.get(cod)

    # Devuelve la lista de estudiantes registrados.
    def listar(self) -> list[Estudiante]:

        # Convierte los valores del diccionario en una lista.
        return list(self._datos.values())

    # Elimina un estudiante por su código.
    def eliminar(self, cod: int) -> None:

        # Elimina el registro si existe.
        self._datos.pop(cod, None)

        # Guarda el archivo actualizado.
        self._persistir()
