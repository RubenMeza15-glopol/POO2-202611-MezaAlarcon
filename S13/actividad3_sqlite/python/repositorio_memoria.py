
# SEMANA 13 - ACTIVIDAD 3
# REPOSITORIO EN MEMORIA

# Permite indicar que buscar puede devolver None.
from typing import Optional

# Importa el modelo Estudiante.
from estudiante import Estudiante


# Repositorio que almacena estudiantes en memoria.
class RepositorioMemoria:

    # Constructor.
    def __init__(self) -> None:

        # Diccionario para guardar estudiantes por código.
        self._datos: dict[int, Estudiante] = {}

    # Guarda un estudiante.
    def guardar(self, e: Estudiante) -> None:

        # Almacena al estudiante usando su código.
        self._datos[e.codigo] = e

    # Busca un estudiante por código.
    def buscar(self, cod: int) -> Optional[Estudiante]:

        # Devuelve el estudiante o None si no existe.
        return self._datos.get(cod)

    # Lista todos los estudiantes.
    def listar(self) -> list[Estudiante]:

        # Devuelve una lista de los estudiantes.
        return list(self._datos.values())
